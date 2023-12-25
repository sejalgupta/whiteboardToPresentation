import { useState } from "react";
import AudioRecorder from "./AudioRecorder";

export default function Form() {
    const [audioBlob, setAudioBlob] = useState<Blob>();
    const [transcript, setTranscript] = useState<string>("");

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
        formData.append("audioBlob", audioBlob);
        const response = await fetch("http://localhost:3001/api/uploadAudio", {
            method: "POST",
            body: formData,
            mode: "cors",
        });
        const data = await response.json();
        console.log(data);
        setTranscript(data.transcript);
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
                { transcript && <p>{transcript}</p> }
                
            </form>
        </div>
    );
}