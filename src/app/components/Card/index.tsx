"use client"
import { useState } from 'react';
import MUICard from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { Button, CardActionArea, CardActions } from '@mui/material';
import FormDialog from "./FormDialog"
import { scheduleAtom } from "@/app/atoms"
import { useAtom } from 'jotai'

type Props = {
    column: number;
    row: number;
}

export default function Card({ column, row }: Props) {
    const [open, setOpen] = useState(false);
    const [schedule, setSchedule] = useAtom(scheduleAtom)
    const scheduleKey = `${row}${column}`

    const handleClickOpen = () => {
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
    };

    return (
        <>
            <MUICard>
                <CardActionArea sx={{ aspectRatio: 5 / 3 }} onClick={handleClickOpen}>
                    <CardContent>
                        <Typography component="div" sx={{ whiteSpace: "nowrap", textOverflow: "ellipsis", overflow: "hidden" }}>
                            {schedule[scheduleKey]?.title}
                        </Typography>
                        <Typography component="div" sx={{ whiteSpace: "nowrap", textOverflow: "ellipsis", overflow: "hidden" }}>
                            {schedule[scheduleKey]?.place}
                        </Typography>
                    </CardContent>
                </CardActionArea>
            </MUICard>
            <FormDialog open={open} handleClose={handleClose} column={column} row={row}></FormDialog>
        </>
    );
}