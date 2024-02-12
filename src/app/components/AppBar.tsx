import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import GoogleButton from "@/app/components/GoogleButtons"
import { AppName } from "@/app/constant";

export default function ButtonAppBar() {
    return (
        <Box sx={{ flexGrow: 1 }}>
            <AppBar position="fixed" elevation={0} color="secondary" sx={{ borderBottom: '1px solid #d0d0d0' }}>
                <Toolbar>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        {AppName}
                    </Typography>
                    <GoogleButton></GoogleButton>
                </Toolbar>
            </AppBar>
            <Toolbar />
        </Box>
    );
}

