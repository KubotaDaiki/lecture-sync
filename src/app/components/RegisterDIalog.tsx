import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import LinearProgress from '@mui/material/LinearProgress';

type Props = {
    open: boolean;
    isLoading: boolean;
    handleCancel: () => void;
    handleOK: () => void;
}

export default function FormDialog({ open, isLoading, handleCancel, handleOK }: Props) {
    return (
        <>
            <Dialog
                open={open}
                onClose={handleCancel}
            >
                <DialogTitle>カレンダーに予定を登録しますか？</DialogTitle>
                {isLoading && <DialogContent><LinearProgress /></DialogContent>}
                <DialogActions>
                    <Button onClick={handleCancel}>キャンセル</Button>
                    <Button onClick={handleOK}>登録</Button>
                </DialogActions>
            </Dialog >
        </>
    );
}