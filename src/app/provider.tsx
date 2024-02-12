import { SessionContextProvider } from "@supabase/auth-helpers-react";
import { createClient } from "@supabase/supabase-js";
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { jaJP } from '@mui/x-date-pickers/locales';
import { jaJP as coreJaJP } from '@mui/material/locale';
import { ReactNode } from 'react';

const supabase = createClient(
    "https://nbaenehsinowupeeyhhl.supabase.co",
    process.env.NEXT_PUBLIC_SUPABASE_KEY!
);


const theme = createTheme(
    {
        palette: {
            secondary: { main: '#ffffff' },
        },
    },
    jaJP,
    coreJaJP
);

export default function Provider({ children }: { children: ReactNode }) {
    return (
        <ThemeProvider theme={theme}>
            <SessionContextProvider supabaseClient={supabase}>
                {children}
            </SessionContextProvider>
        </ThemeProvider>
    )
}