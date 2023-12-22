import { useState } from "react";
import AudioRecorder from "./AudioRecorder";

export default function Form() {
    const [audioBlob, setAudioBlob] = useState<Blob>();

    const setAudioBlobWrapper = (blob: Blob | undefined) => {
        setAudioBlob(blob);
    }

    const submitForm = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (!audioBlob) {
            console.error("No audio blob.");
            return;
        }
        const formData = new FormData();
        formData.append("audio", audioBlob);
        const response = await fetch("http://localhost:3001/api/upload", {
            method: "POST",
            body: formData
        });
        const data = await response.json();
        console.log(data);
    }

    return (
        <div className="Form">
            <form method="POST" onSubmit={submitForm}>
                <AudioRecorder setAudioBlob={setAudioBlobWrapper} />
                { audioBlob && (
                    <>
                        <audio src={URL.createObjectURL(audioBlob)} controls />
                        <br />
                        <input type="submit" value="Upload" />
                    </>
                )}
                
            </form>
        </div>
    );
}