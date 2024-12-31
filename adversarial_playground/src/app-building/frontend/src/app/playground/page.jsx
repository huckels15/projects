'use client';

import React, { useState } from "react";
import { getFGSMres } from '@/components/playground/FGSMres';
import { getPGDres } from '@/components/playground/PGDres';
import { getDEEPFOOLres } from '@/components/playground/DEEPFOOLres';
import { getSQUAREres } from '@/components/playground/SQUAREres';
import { getFGSMalex } from '@/components/playground/FGSMalex';
import { getPGDalex } from '@/components/playground/PGDalex';
import { getDEEPFOOLalex } from '@/components/playground/DEEPFOOLalex';
import { getSQUAREalex } from '@/components/playground/SQUAREalex';
import { getFGSMresrob } from '@/components/playground/FGSMresrob';
import { getPGDresrob } from '@/components/playground/PGDresrob';
import { getDEEPFOOLresrob } from '@/components/playground/DEEPFOOLresrob';
import { getSQUAREresrob } from '@/components/playground/SQUAREresrob';
import { getFGSMalexrob } from '@/components/playground/FGSMalexrob';
import { getPGDalexrob } from '@/components/playground/PGDalexrob';
import { getDEEPFOOLalexrob } from '@/components/playground/DEEPFOOLalexrob';
import { getSQUAREalexrob } from '@/components/playground/SQUAREalexrob';
import { getFGSMcustom} from '@/components/playground/FGSMcustom';
import { getPGDcustom} from '@/components/playground/PGDcustom';
import { getDEEPFOOLcustom} from '@/components/playground/DEEPFOOLcustom';
import { getSQUAREcustom} from '@/components/playground/SQUAREcustom';

export default function PlaygroundPage() {
    const [selectedModel, setSelectedModel] = useState('');
    const [selectedAttack, setSelectedAttack] = useState('');
    const [additionalValues, setAdditionalValues] = useState({});
    const [regAcc, setRegAcc] = useState(null);
    const [advAcc, setAdvAcc] = useState(null);
    const [plotOutput, setPlotOutput] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleModelChange = (event) => {
        setSelectedModel(event.target.value);
        setSelectedAttack(''); // Reset attack selection
        setAdditionalValues({}); // Reset additional values
    };

    const handleAttackChange = (event) => {
        setSelectedAttack(event.target.value);
        setAdditionalValues({}); // Reset additional values
    };

    const handleAdditionalValueChange = (key, value) => {
        setAdditionalValues((prev) => ({ ...prev, [key]: value }));
    };

    const handleRun = async () => {
        if (selectedModel && selectedAttack) {
            setLoading(true);
            setError(null);
            try {
                let result;

                // Call the appropriate function based on the selected attack
                if (selectedModel === "resnet" && selectedAttack === "fgsm") {
                    result = await getFGSMres(selectedModel, selectedAttack, additionalValues);
                } else if (selectedModel === "resnet" && selectedAttack === "pgd") {
                    result = await getPGDres(selectedModel, selectedAttack, additionalValues);
                } else if (selectedModel === "resnet" && selectedAttack === "deepfool") {
                    result = await getDEEPFOOLres(selectedModel, selectedAttack, additionalValues);
                } else if (selectedModel === "resnet" && selectedAttack === "square") {
                    result = await getSQUAREres(selectedModel, selectedAttack, additionalValues);
                } else if (selectedModel === "alexnet" && selectedAttack === "fgsm") {
                    result = await getFGSMalex(selectedModel, selectedAttack, additionalValues);
                } else if (selectedModel === "alexnet" && selectedAttack === "pgd") {
                    result = await getPGDalex(selectedModel, selectedAttack, additionalValues);
                } else if (selectedModel === "alexnet" && selectedAttack === "deepfool") {
                    result = await getDEEPFOOLalex(selectedModel, selectedAttack, additionalValues);
                } else if (selectedModel === "alexnet" && selectedAttack === "square") {
                    result = await getSQUAREalex(selectedModel, selectedAttack, additionalValues);
                } else if (selectedModel === "resnetrob" && selectedAttack === "fgsm") {
                    result = await getFGSMresrob("robust_resnet", selectedAttack, additionalValues);
                } else if (selectedModel === "resnetrob" && selectedAttack === "pgd") {
                    result = await getPGDresrob("robust_resnet", selectedAttack, additionalValues);
                } else if (selectedModel === "resnetrob" && selectedAttack === "deepfool") {
                    result = await getDEEPFOOLresrob("robust_resnet", selectedAttack, additionalValues);
                } else if (selectedModel === "resnetrob" && selectedAttack === "square") {
                    result = await getSQUAREresrob("robust_resnet", selectedAttack, additionalValues);
                } else if (selectedModel === "alexnetrob" && selectedAttack === "fgsm") {
                    result = await getFGSMalexrob("robust_alexnet", selectedAttack, additionalValues);
                } else if (selectedModel === "alexnetrob" && selectedAttack === "pgd") {
                    result = await getPGDalexrob("robust_alexnet", selectedAttack, additionalValues);
                } else if (selectedModel === "alexnetrob" && selectedAttack === "deepfool") {
                    result = await getDEEPFOOLalexrob("robust_alexnet", selectedAttack, additionalValues);
                } else if (selectedModel === "alexnetrob" && selectedAttack === "square") {
                    result = await getSQUAREalexrob("robust_alexnet", selectedAttack, additionalValues);
                } else if (selectedModel === "custom" && selectedAttack === "fgsm") {
                    result = await getFGSMcustom(selectedModel, selectedAttack, additionalValues);
                } else if (selectedModel === "custom" && selectedAttack === "pgd") {
                    result = await getPGDcustom(selectedModel, selectedAttack, additionalValues);
                } else if (selectedModel === "custom" && selectedAttack === "deepfool") {
                    result = await getDEEPFOOLcustom(selectedModel, selectedAttack, additionalValues);
                } else if (selectedModel === "custom" && selectedAttack === "square") {
                    result = await getSQUAREcustom(selectedModel, selectedAttack, additionalValues);
                }

                if (result.error) {
                    setError("Failed to fetch response.");
                } else {
                    setRegAcc(result.regAcc);
                    setAdvAcc(result.advAcc);
                    setPlotOutput(result.decodedImage);
                }
            } catch (err) {
                setError("An error occurred while fetching the response.");
                console.error(err.message);
            } finally {
                setLoading(false);
            }
        } else {
            setError("Please select both a model and an attack.");
        }
    };

    const renderAdditionalInputs = () => {
        if (!selectedModel || !selectedAttack) return null;
    
        return (
            <div className="mt-8">
                <h2 className="text-xl font-bold text-green-400">Additional Settings</h2>
                <div className="mt-4 space-y-4">
                    {selectedModel === "custom" && (
                        <>
                            <div>
                                <label className="block text-green-600 font-semibold">Model Name (No Extension):</label>
                                <input
                                    type="text"
                                    value={additionalValues.modelName || ''}
                                    onChange={(e) => handleAdditionalValueChange('modelName', e.target.value)}
                                    className="w-full px-4 py-2 bg-gray-900 text-green-400 border border-green-600 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-green-500"
                                />
                            </div>
                            <div>
                                <label className="block text-green-600 font-semibold">Dataset Name (No Extension):</label>
                                <input
                                    type="text"
                                    value={additionalValues.datasetName || ''}
                                    onChange={(e) => handleAdditionalValueChange('datasetName', e.target.value)}
                                    className="w-full px-4 py-2 bg-gray-900 text-green-400 border border-green-600 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-green-500"
                                />
                            </div>
                            <div>
                                <label className="block text-green-600 font-semibold">Width:</label>
                                <input
                                    type="number"
                                    min="1"
                                    value={additionalValues.width || ''}
                                    onChange={(e) => handleAdditionalValueChange('width', e.target.value)}
                                    className="w-full px-4 py-2 bg-gray-900 text-green-400 border border-green-600 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-green-500"
                                />
                            </div>
                            <div>
                                <label className="block text-green-600 font-semibold">Height:</label>
                                <input
                                    type="number"
                                    min="1"
                                    value={additionalValues.height || ''}
                                    onChange={(e) => handleAdditionalValueChange('height', e.target.value)}
                                    className="w-full px-4 py-2 bg-gray-900 text-green-400 border border-green-600 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-green-500"
                                />
                            </div>
                            <div>
                                <label className="block text-green-600 font-semibold">Channels:</label>
                                <input
                                    type="number"
                                    min="1"
                                    value={additionalValues.channels || ''}
                                    onChange={(e) => handleAdditionalValueChange('channels', e.target.value)}
                                    className="w-full px-4 py-2 bg-gray-900 text-green-400 border border-green-600 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-green-500"
                                />
                            </div>
                        </>
                    )}
    
                    {/* Attack-specific inputs */}
                    {selectedAttack === "fgsm" && (
                        <div>
                            <label className="block text-green-600 font-semibold">Epsilon (Perturbation Strength):</label>
                            <input
                                type="number"
                                step="0.01"
                                min="0"
                                value={additionalValues.epsilon || ''}
                                onChange={(e) => handleAdditionalValueChange('epsilon', e.target.value)}
                                className="w-full px-4 py-2 bg-gray-900 text-green-400 border border-green-600 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-green-500"
                            />
                        </div>
                    )}
                    {selectedAttack === "pgd" && (
                        <>
                            <div>
                                <label className="block text-green-600 font-semibold">Epsilon (Perturbation Strength):</label>
                                <input
                                    type="number"
                                    step="0.01"
                                    min="0"
                                    value={additionalValues.epsilon || ''}
                                    onChange={(e) => handleAdditionalValueChange('epsilon', e.target.value)}
                                    className="w-full px-4 py-2 bg-gray-900 text-green-400 border border-green-600 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-green-500"
                                    />
                            </div>
                            <div>
                                <label className="block text-green-600 font-semibold">Max Iterations:</label>
                                <input
                                    type="number"
                                    min="1"
                                    value={additionalValues.maxIterations || ''}
                                    onChange={(e) => handleAdditionalValueChange('maxIterations', e.target.value)}
                                    className="w-full px-4 py-2 bg-gray-900 text-green-400 border border-green-600 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-green-500"
                                    />
                            </div>
                            <div>
                                <label className="block text-green-600 font-semibold">Step Size:</label>
                                <input
                                    type="number"
                                    step="0.01"
                                    min="0"
                                    value={additionalValues.stepSize || ''}
                                    onChange={(e) => handleAdditionalValueChange('stepSize', e.target.value)}
                                    className="w-full px-4 py-2 bg-gray-900 text-green-400 border border-green-600 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-green-500"
                                    />
                            </div>
                        </>
                    )}
                    {selectedAttack === "deepfool" && (
                        <div>
                            <label className="block text-green-600 font-semibold">Max Iterations:</label>
                            <input
                                type="number"
                                min="1"
                                value={additionalValues.maxIterations || ''}
                                onChange={(e) => handleAdditionalValueChange('maxIterations', e.target.value)}
                                className="w-full px-4 py-2 bg-gray-900 text-green-400 border border-green-600 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-green-500"
                            />
                        </div>
                    )}
                    {selectedAttack === "square" && (
                        <>
                            <div>
                                <label className="block text-green-600 font-semibold">Epsilon (Perturbation Strength):</label>
                                <input
                                    type="number"
                                    step="0.01"
                                    min="0"
                                    value={additionalValues.epsilon || ''}
                                    onChange={(e) => handleAdditionalValueChange('epsilon', e.target.value)}
                                    className="w-full px-4 py-2 bg-gray-900 text-green-400 border border-green-600 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-green-500"
                                    />
                            </div>
                            <div>
                                <label className="block text-green-600 font-semibold">Max Iterations:</label>
                                <input
                                    type="number"
                                    min="1"
                                    value={additionalValues.maxIterations || ''}
                                    onChange={(e) => handleAdditionalValueChange('maxIterations', e.target.value)}
                                    className="w-full px-4 py-2 bg-gray-900 text-green-400 border border-green-600 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-green-500"
                                    />
                            </div>
                        </>
                    )}
                </div>
            </div>
        );
    };
    
    

    return (
        <div className="min-h-screen bg-black text-green-400 pt-20 pb-12 px-4">
            <div className="container mx-auto max-w-6xl">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {/* User Selection */}
                    <div>
                        {/* Select Model */}
                        <div className="mb-8">
                            <h1 className="text-2xl md:text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-green-400 via-green-500 to-green-600 font-mono">
                                Select a Model
                            </h1>
                            <div className="mt-4">
                                <select
                                    value={selectedModel}
                                    onChange={handleModelChange}
                                    className="w-full px-4 py-2 bg-gray-900 text-green-400 border border-green-600 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-green-500"
                                >
                                    <option value="" disabled>
                                        Choose a Model
                                    </option>
                                    <option value="resnet">ResNet</option>
                                    <option value="alexnet">AlexNet</option>
                                    <option value="resnetrob">ResNet - Robust</option>
                                    <option value="alexnetrob">AlexNet - Robust</option>
                                    <option value="custom">Custom Attack</option>
                                </select>
                            </div>
                        </div>

                        {/* Select Attack */}
                        <div className="mb-8">
                            <h1 className="text-2xl md:text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-green-400 via-green-500 to-green-600 font-mono">
                                Select an Attack
                            </h1>
                            <div className="mt-4">
                                <select
                                    value={selectedAttack}
                                    onChange={handleAttackChange}
                                    className="w-full px-4 py-2 bg-gray-900 text-green-400 border border-green-600 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-green-500"
                                >
                                    <option value="" disabled>
                                        Choose an Attack
                                    </option>
                                    <option value="fgsm">Fast Gradient Sign Method</option>
                                    <option value="pgd">Projected Gradient Descent</option>
                                    <option value="deepfool">DeepFool</option>
                                    <option value="square">Square Attack</option>
                                </select>
                            </div>
                        </div>

                        {/* Additional Inputs */}
                        {renderAdditionalInputs()}
                    </div>

                    {/* Display Backend Output */}
                    <div className="flex flex-col items-center justify-center">
                        <button
                            onClick={handleRun}
                            className="mb-8 px-6 py-2 bg-green-700 text-black font-bold rounded-lg shadow-lg hover:bg-green-600 transition-transform transform hover:scale-105"
                        >
                            Let's Play!
                        </button>

                        <div className="text-center">
                            {loading ? (
                                <p className="text-green-400">Loading...</p>
                            ) : error ? (
                                <p className="text-red-500">{error}</p>
                            ) : (
                                <>
                                    {regAcc !== null && advAcc !== null && (
                                        <div className="bg-gray-900 p-4 rounded-lg shadow-inner text-left">
                                            <p>
                                                <span className="font-bold">Accuracy Before Attack:</span> {regAcc}
                                            </p>
                                            <p>
                                                <span className="font-bold">Accuracy After Attack:</span> {advAcc}
                                            </p>
                                        </div>
                                    )}

                                    {plotOutput && (
                                        <img
                                            src={plotOutput}
                                            alt="Adversarial Output"
                                            className="mt-4 max-w-full rounded-lg shadow-md"
                                        />
                                    )}
                                </>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}