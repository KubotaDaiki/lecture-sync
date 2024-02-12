import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import { Stack } from '@mui/material';
import { scheduleAtom } from "@/app/atoms"
import { useAtom } from 'jotai'
import { WEEKS } from '@/app/constant';

type Props = {
    open: boolean;
    handleClose: () => void;
    column: number
    row: number
}

export default function FormDialog({ open, handleClose, column, row }: Props) {
    const [schedule, setSchedule] = useAtom(scheduleAtom)
    const scheduleKey = `${row}${column}`

    return (
        <>
            <Dialog
                open={open}
                onClose={handleClose}
                PaperProps={{
                    component: 'form',
                    onSubmit: (event: React.FormEvent<HTMLFormElement>) => {
                        event.preventDefault();
                        const formData = new FormData(event.currentTarget);
                        const formJson = Object.fromEntries((formData as any).entries());
                        setSchedule({ ...schedule, [scheduleKey]: { title: formJson.title, place: formJson.place } })
                        handleClose();
                    },
                }}
            >
                <DialogTitle>{`${WEEKS[column]}曜${row + 1}限`}</DialogTitle>
                <DialogContent>
                    <Stack spacing={2} sx={{ width: "400px" }}>
                        <DialogContentText>
                            予定を入力してください。
                        </DialogContentText>
                        <TextField
                            autoFocus
                            name="title"
                            label="講義名"
                            fullWidth
                            variant="standard"
                            defaultValue={schedule[scheduleKey]?.title}
                        />
                        <TextField
                            autoFocus
                            name="place"
                            label="場所"
                            fullWidth
                            variant="standard"
                            defaultValue={schedule[scheduleKey]?.place}
                        />
                    </Stack>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleClose}>キャンセル</Button>
                    <Button type="submit">OK</Button>
                </DialogActions>
            </Dialog >
        </>
    );
}