'use client';

import { useState } from 'react';
import { uploadModel } from '@/components/upload/uploadModel';
import { uploadData } from '@/components/upload/uploadData';

export default function UploadPage() {
    const [modelFile, setModelFile] = useState(null);
    const [datasetFile, setDatasetFile] = useState(null);
    const [uploadStatus, setUploadStatus] = useState('');
    const [loading, setLoading] = useState(false);

    const handleModelUpload = (event) => {
        setModelFile(event.target.files[0]);
    };

    const handleDatasetUpload = (event) => {
        setDatasetFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!modelFile || !datasetFile) {
            setUploadStatus('Please upload both a model file and a dataset file.');
            return;
        }

        // const formData = new FormData();
        // formData.append('model', modelFile);
        // formData.append('dataset', datasetFile);

        setLoading(true);
        setUploadStatus('');

        try {
            const modelResponse = await uploadModel(modelFile);
            const dataResponse = await uploadData(datasetFile);

            if (modelResponse.success && dataResponse.success) {
                setUploadStatus('Model and dataset uploaded successfully!');
            } else {
                setUploadStatus('Failed to upload model or dataset.');
            }
        } catch (error) {
            setUploadStatus('An error occurred during upload.');
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-black text-green-400 pt-20 pb-12 px-4">
            <div className="container mx-auto max-w-4xl">
                <h1 className="text-3xl font-bold text-center mb-8 bg-clip-text text-transparent bg-gradient-to-r from-green-400 via-green-500 to-green-600">Upload Model and Dataset</h1>
                <div className="space-y-6">
                    {/* Model Upload */}
                    <div>
                        <label
                            htmlFor="model-upload"
                            className="block text-lg font-medium text-green-400 mb-2"
                        >
                            Upload Model (.h5)
                        </label>
                        <input
                            type="file"
                            id="model-upload"
                            accept=".h5"
                            onChange={handleModelUpload}
                            className="w-full bg-grey-900 text-green-400 border border-green-600 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-green-500"
                        />
                    </div>

                    {/* Dataset Upload */}
                    <div>
                        <label
                            htmlFor="dataset-upload"
                            className="block text-lg font-medium text-green-400 mb-2"
                        >
                            Upload Dataset (.zip)
                        </label>
                        <input
                            type="file"
                            id="dataset-upload"
                            accept=".zip"
                            onChange={handleDatasetUpload}
                            className="w-full bg-black text-green-400 border border-green-600 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-green-500"
                        />
                    </div>

                    {/* Upload Button */}
                    <div className="text-center">
                        <button
                            onClick={handleUpload}
                            className="px-6 py-2 bg-green-700 text-black font-bold rounded-lg shadow-lg hover:bg-green-600 transition-transform transform hover:scale-105"
                            disabled={loading}
                        >
                            {loading ? 'Uploading...' : 'Upload Files'}
                        </button>
                    </div>

                    {/* Status Display */}
                    {uploadStatus && (
                        <div
                            className={`mt-4 text-center text-lg font-medium ${
                                uploadStatus.includes('successfully')
                                    ? 'text-green-500'
                                    : 'text-red-500'
                            }`}
                        >
                            {uploadStatus}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}