'use client';

export default function AttacksPage() {
    return (
        <div className="min-h-screen bg-black text-green-400 relative overflow-hidden">

            {/* Main Content */}
            <div className="relative z-10 container mx-auto max-w-6xl py-20 text-center">
                {/* Header Spot */}
                <div className="mb-12">
                    <h1 className="text-4xl md:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-green-400 via-green-500 to-green-600 font-mono">
                        Types of Adversarial Attacks
                    </h1>
                </div>

                {/* Types of Attacks */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                    {/* FGSM */}
                    <div className="p-6 bg-gray-900 border border-green-500 rounded-lg shadow-md hover:shadow-green-500/50 transition-transform duration-300 transform hover:scale-105">
                        <h2 className="text-xl font-bold text-green-400 mt-4">Fast Gradient Sign Method</h2>
                        <p className="text-green-500 mt-4">
                            The Fast Gradient Sign Method (FGSM) is an adversarial attack which slightly
                            changes the input data through adding noise based on the gradient of the loss
                            with respect to the input image. While the input will look similar if not identical
                            to the human eye, the attack affects the model by forcing it to misclassify the data. Visit <a href="https://medium.com/@zachariaharungeorge/a-deep-dive-into-the-fast-gradient-sign-method-611826e34865" 
                            className="text-green-300 underline hover:text-green-200 transition-colors" target="_blank" rel="noopener noreferrer">
                            A Deep Dive into the Fast Gradient Design Method </a>
                             to learn more.
                        </p>
                    </div>

                    {/* PGD */}
                    <div className="p-6 bg-gray-900 border border-green-500 rounded-lg shadow-md hover:shadow-green-500/50 transition-transform duration-300 transform hover:scale-105">
                        <h2 className="text-xl font-bold text-green-400 mt-4">Projected Gradient Descent</h2>
                        <p className="text-green-500 mt-4">
                            The Projected Gradient Descent (PGD) attack is similar to the Fast Gradient Sign 
                            method in that an input image is changed based on the model's gradient. It is another white-box 
                            method that requires full knowledge of how a model functions. Read more about the 
                            PGD method here: <a href="https://medium.com/@zachariaharungeorge/a-deep-dive-into-the-fast-gradient-sign-method-611826e34865" 
                            className="text-green-300 underline hover:text-green-200 transition-colors" target="_blank" rel="noopener noreferrer">
                            Unveiling the Power of Projected Gradient Descent in Adversarial Attacks.</a>
                        </p>
                    </div>

                    {/* DeepFool */}
                    <div className="p-6 bg-gray-900 border border-green-500 rounded-lg shadow-md hover:shadow-green-500/50 transition-transform duration-300 transform hover:scale-105">
                        <h2 className="text-xl font-bold text-green-400 mt-4">DeepFool</h2>
                        <p className="text-green-500 mt-4">
                            The DeepFool attack is an adversarial attack which aims to "create the most minimal perturbations
                            to an image to deceive (a) model". It aims to find a point across a decision boundary that is 
                            the closest to the original input to cause a model to misclassify the input with the least 
                            amount of modification possible. You can read the paper <a href="https://ieeexplore.ieee.org/document/10134485" 
                            className="text-green-300 underline hover:text-green-200 transition-colors" target="_blank" rel="noopener noreferrer">
                            Understanding DeepFool Adversarial Attack and Defense with Skater Interpretations </a> to learn more.
                        </p>
                    </div>

                    {/* Square */}
                    <div className="p-6 bg-gray-900 border border-green-500 rounded-lg shadow-md hover:shadow-green-500/50 transition-transform duration-300 transform hover:scale-105">
                        <h2 className="text-xl font-bold text-green-400 mt-4">Square Attack</h2>
                        <p className="text-green-500 mt-4">
                            The Square Attack is a black-box attack that enables a user to not need to know the entirety 
                            of how a model works. The attack changes an image by adding square-shaped contiguous
                            pixels, hence the name Square Attack, to an image where once again the change is imperceptible 
                            to the human eye, but to a model the change is enough to misclassify the input. 
                            You can read more about the Square Attack here: <a href="https://arxiv.org/pdf/2201.05001#:~:text=In%20white%2Dbox%20attack%2C%20adversary,interact%20through%20input%20and%20output." 
                            className="text-green-300 underline hover:text-green-200 transition-colors" target="_blank" rel="noopener noreferrer">
                            Evaluation of Four Black-box Adversarial Attacks and Some Query-efficient Improvement Analysis.</a>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
