import { useState } from "react";
import AudioRecorder from "./AudioRecorder";

export default function Form() {
    const [recordAudio, setRecordAudio] = useState<boolean>(true);
    const [audioBlob, setAudioBlob] = useState<Blob>();
    const [transcript, setTranscript] = useState<string>("");
    const [presentationLink, setPresentationLink] = useState<string>("");

    const setAudioBlobWrapper = (blob: Blob | undefined) => {
        setAudioBlob(blob);
    }

    const submitForm = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (!audioBlob) {
            console.error("No audio blob.");
            return;
        }

        const formData = new FormData(event.nativeEvent.target as HTMLFormElement);
        if (audioBlob) {
            formData.append("audioBlob", audioBlob);
        }
        const response = await fetch("http://localhost:3001/api/uploadAudio", {
            method: "POST",
            body: formData,
            mode: "cors",
        });
        const data = await response.json();
        console.log(data);
        setTranscript(data.transcript);
        setPresentationLink("http://localhost:3001/" + data.presentation);
    }

    return (
        <div id="form" className="max-w-lg mx-auto text-left">
            <h1 className="text-3xl text-center font-bold text-gray-900 my-6">Create a Presentation</h1>
            <form method="POST" onSubmit={submitForm}>
                <div className="py-3">
                    <label htmlFor="topic" className="block text-sm font-bold leading-6 text-gray-900">
                        Topic
                    </label>
                    <div className="relative mt-2 rounded-md shadow-sm">
                        <input
                        type="text"
                        name="topic"
                        id="topic"
                        className="block w-full rounded-md border-0 py-1.5 px-3 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                        placeholder="Photosynthesis"
                        />
                    </div>
                </div>
                <div className="py-3">
                    <label htmlFor="role" className="block text-sm font-bold leading-6 text-gray-900">
                        Role
                    </label>
                    <div className="relative mt-2 rounded-md shadow-sm">
                        <input
                        type="text"
                        name="role"
                        id="role"
                        className="block w-full rounded-md border-0 py-1.5 px-3 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                        placeholder="Teacher for sixth grade science class"
                        />
                    </div>
                </div>
                <div className="py-3">
                    <label htmlFor="text_context" className="block text-sm font-bold leading-6 text-gray-900">
                        Presentation Context
                    </label>
                    <div className="relative mt-2 rounded-md shadow-sm">
                        <textarea
                        id="text_context"
                        name="text_context"
                        rows={3}
                        className="block w-full rounded-md border-0 py-1.5 px-3 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                        defaultValue={''}
                        />
                    </div>
                    <p className="mt-3 text-sm leading-6 text-gray-600">
                        Describe the context of the presentation. For example, what you are going to use it for, how you want to focus on, etc.
                    </p>
                </div>
                <div className="py-3">
                    <label htmlFor="length" className="block text-sm font-bold leading-6 text-gray-900">
                        Length of presentation
                    </label>
                    <div className="relative mt-2 rounded-md shadow-sm">
                        <input
                        type="number"
                        name="length"
                        id="length"
                        className="inline-block rounded-md border-0 py-1.5 px-3 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                        placeholder="10"
                        /> minutes
                    </div>
                </div>
                <div className="py-3">
                    <label className="relative inline-flex items-center cursor-pointer">
                        <input
                            type="checkbox"
                            value="record"
                            className="sr-only peer"
                            checked={recordAudio}
                            onChange={() => setRecordAudio(!recordAudio)}
                        />
                        <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                        <span className="ms-3 text-sm font-medium">Record Audio</span>
                    </label>
                </div>
                { recordAudio && (
                    <div className="py-3 px-5 outline outline-gray-200 rounded-md">
                        <AudioRecorder setAudioBlob={setAudioBlobWrapper} />
                        { audioBlob && (
                            <div className="py-3">
                                <audio src={URL.createObjectURL(audioBlob)} controls />
                                {/* <br />
                                <input type="submit" value="Upload" /> */}
                            </div>
                        )}
                        { transcript && (
                            <div className="py-3">
                                <label htmlFor="audio-transcript" className="block text-sm font-bold leading-6 text-gray-900">
                                    Audio Transcript
                                </label>
                                <div className="relative rounded-md shadow-sm">
                                    <textarea
                                    id="audio-transcript"
                                    name="audio-transcript"
                                    rows={5}
                                    disabled
                                    className="block w-full rounded-md border-0 py-1.5 px-3 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                                    defaultValue={transcript}
                                    />
                                </div>
                            </div>
                        ) }
                    </div>
                ) }
                <div className="py-3">
                    { presentationLink ? (
                        <a href={presentationLink} className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">
                            Download Presentation
                        </a>
                    ) : (
                        <button type="submit" className="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                            Create Presentation
                        </button>
                    ) }
                </div>
            </form>
        </div>
    );
}