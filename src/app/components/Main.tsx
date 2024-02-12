import Grid from '@mui/material/Unstable_Grid2';
import { ReactNode } from 'react';

export default function Main({ children }: { children: ReactNode }) {
    return (
        <Grid container
            spacing={2}
            justifyContent="center"
            alignItems="center"
            columns={8}
            sx={{ minWidth: "700px", maxWidth: "1200px" }}
        >
            {children}
        </Grid>
    )
}