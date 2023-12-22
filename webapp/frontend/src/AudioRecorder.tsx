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
        <div className="AudioRecorder">
            <p>AudioRecorder</p>
            {recording ? (
                <button onClick={stopRecording} type="button">Stop Recording</button>
            ) : (
                <button onClick={startRecording} type="button">Start Recording</button>
            )}
            <br />
        </div>
    );
}