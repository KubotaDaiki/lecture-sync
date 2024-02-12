import Grid from '@mui/material/Unstable_Grid2';
import Card from '@/app/components/Card';
import { WEEKS } from '@/app/constant';

type Xs = { xs: number }

export default function Timetable({ xs }: Xs) {
    return (
        [...Array(6)].map((_, row) => {
            return (
                WEEKS.map((v, column) => {
                    if (column === 0) {
                        return (
                            <Grid xs={xs} key={v}>
                                <p style={{ textAlign: "center", padding: "5px" }}>{`${row + 1}限`}</p>
                            </Grid>
                        )
                    }

                    return (
                        <Grid xs={xs} key={v}>
                            <Card column={column} row={row}></Card>
                        </Grid>
                    )
                }))
        })
    )
}