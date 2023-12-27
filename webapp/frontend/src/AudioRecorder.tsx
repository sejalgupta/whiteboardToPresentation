import { useState, useRef } from 'react';
import RecordRTCPromisesHandler from 'recordrtc';

type setAudioBlobType = (blob: Blob | undefined) => void;

export default function AudioRecorder( props: { setAudioBlob: setAudioBlobType }) {
    let recorder = useRef<RecordRTCPromisesHandler>();
    let mediaStream = useRef<MediaStream>();
    const [recording, setRecording] = useState<boolean>(false);
    const startRecording = async () => {
        props.setAudioBlob(undefined);
        mediaStream.current = await navigator.mediaDevices.getUserMedia({audio: true});
        recorder.current = new RecordRTCPromisesHandler(mediaStream.current, {
            type: 'audio'
        });
        recorder.current.startRecording();
        setRecording(true);
    }

    const stopRecording = async () => {
        if (!recorder.current) {
            console.error("Recorder is not initialized.");
            return;
        }
        await recorder.current.stopRecording(async () => {
            if (!recorder.current) {
                console.error("Recorder is not initialized.");
                return;
            }
            setRecording(false);
            const blob = await recorder.current.getBlob();
            mediaStream.current?.getTracks().forEach(track => track.stop());
            props.setAudioBlob(blob);
        });
    }

    return (
        <div id="audio-recorder">
            {recording ? (
                <button type="button" className="rounded-md outline outline-red-500 px-3 py-2 text-sm font-semibold text-red-500 shadow-sm hover:bg-red-500 hover:text-white" onClick={stopRecording}>
                    Stop Recording
                </button>
            ) : (
                <button type="button" className="rounded-md outline outline-red-500 px-3 py-2 text-sm font-semibold text-red-500 shadow-sm hover:bg-red-500 hover:text-white" onClick={startRecording}>
                    Start Recording
                </button>
            )}
        </div>
    );
}