from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import subprocess
import os
import json
from typing import Optional
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

class AttackRequest(BaseModel):
    model: str
    attack: str
    epsilon: Optional[float] = None
    eps_step: Optional[float] = None
    max_iter: Optional[int] = None

@app.get("/")
def health_check():
    """
    Health check route.
    """
    return {"status": "healthy"}

@app.post("/predict")
def predict(payload: dict):
    """
    Prediction route to handle attack requests and return both JSON results and an image.
    """
    instances = payload.get("instances")
    if not instances or not isinstance(instances, list) or len(instances) == 0:
        raise HTTPException(status_code=400, detail="Invalid payload format. Expected 'instances' as a non-empty list.")

    instance = instances[0]

    try:
        request = AttackRequest(**instance)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid instance format: {str(e)}")

    script_name = f"{request.model}_attacks.py"
    if not os.path.exists(script_name):
        raise HTTPException(status_code=404, detail="Model script not found")
    
    command = ["python3", script_name]

    if request.attack == "fgsm":
        command.append("--fgsm")
    elif request.attack == "pgd":
        command.append("--pgd")
    elif request.attack == "deepfool":
        command.append("--deepfool")
    elif request.attack == "square":
        command.append("--square")
    else:
        raise HTTPException(status_code=400, detail="Invalid attack type")

    if request.epsilon is not None:
        command.extend(["--eps", str(request.epsilon)])
    if request.eps_step is not None:
        command.extend(["--eps_step", str(request.eps_step)])
    if request.max_iter is not None:
        command.extend(["--max_iter", str(request.max_iter)])

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error running script: {e.stderr}")

    try:
        results = json.loads(output)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to decode script output")
    
    image_path = results.get("figure")
    if not image_path or not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Generated image file not found")

    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

    response_content = {
        "predictions": [
            {
                "reg_acc": results.get("reg_acc"),
                "adv_acc": results.get("adv_acc"),
                "figure": image_base64
            }
        ]
    }

    return JSONResponse(content=response_content)