import Grid from '@mui/material/Unstable_Grid2';
import { WEEKS } from '@/app/constant';

type Xs = { xs: number }

export default function WeeksHeader({ xs }: Xs) {
    return (
        WEEKS.map((v, i) => {
            if (i === 0) {
                return (
                    <Grid xs={xs} key={v}>
                        <div></div>
                    </Grid>
                )
            }

            return (
                <Grid xs={xs} key={v}>
                    <p style={{ textAlign: "center" }}>{v}</p>
                </Grid>
            )
        }
        )
    )
}