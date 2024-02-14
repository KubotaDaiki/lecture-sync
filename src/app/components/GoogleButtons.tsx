import Button from '@mui/material/Button';
import GoogleIcon from '@mui/icons-material/Google'
import Avatar from '@mui/material/Avatar';
import {
    useSession,
    useSupabaseClient,
    useSessionContext,
} from "@supabase/auth-helpers-react";
import Cookies from 'js-cookie';
import { useEffect } from 'react';


export default function GoogleButton() {
    const user = useSession()?.user;
    const { isLoading } = useSessionContext();
    const supabase = useSupabaseClient();

    useEffect(() => {
        supabase.auth.onAuthStateChange(async (event, session) => {
            if (session && session.provider_refresh_token) {
                Cookies.set('oauth_provider_refresh_token', session.provider_refresh_token);
            }

            if (event === 'SIGNED_OUT') {
                await fetch(`https://accounts.google.com/o/oauth2/revoke?token=${Cookies.get("oauth_provider_refresh_token")}`)
                Cookies.remove('oauth_provider_refresh_token');
            }
        });

    }, [])

    if (isLoading) {
        return <></>
    }

    if (user) {
        return <LogoutButton imageUrl={user.user_metadata.avatar_url} />
    }
    else {
        return <LoginButton />
    }
}

const LoginButton = () => {
    const supabase = useSupabaseClient();

    async function googleSignIn() {
        const { error } = await supabase.auth.signInWithOAuth({
            provider: "google",
            options: {
                redirectTo: process.env.NEXT_PUBLIC_CLIENT_REDIRECT_URL,
                queryParams: { access_type: 'offline', prompt: 'consent', },
                scopes:
                    "https://www.googleapis.com/auth/calendar.calendarlist.readonly https://www.googleapis.com/auth/calendar.app.created",
            },
        });

        if (error) {
            alert("Error logging in to Google provider with Supabase");
            console.log(error);
        }
    }

    return (
        <Button
            color="inherit"
            variant="outlined"
            startIcon={<GoogleIcon />}
            onClick={async () => {
                await googleSignIn()
            }
            }>
            連携
        </Button >
    );
};

const LogoutButton = ({ imageUrl }: { imageUrl: string }) => {
    const supabase = useSupabaseClient();

    async function signOut() {
        await supabase.auth.signOut();
    }

    return (
        <>
            <Avatar src={imageUrl} sx={{ marginX: "10px" }} />
            <Button color="inherit" variant="outlined" onClick={() => signOut()}>
                ログアウト
            </Button >
        </>
    );
};