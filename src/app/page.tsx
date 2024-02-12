"use client"
import AppBar from '@/app/components/AppBar';
import DateRangeButton from '@/app/components/DateRangeButton';
import Main from "@/app/components/Main";
import RegisterButton from "@/app/components/RegisterButton";
import Timetable from "@/app/components/Timetable";
import WeeksHeader from "@/app/components/WeeksHeader";
import CssBaseline from '@mui/material/CssBaseline';
import Stack from '@mui/material/Stack';
import Provider from "@/app/provider"

export default function Home() {
  return (
    <Provider>
      <CssBaseline />
      <AppBar></AppBar>
      <Stack spacing={2} alignItems="center" sx={{ marginY: "50px" }}>
        <DateRangeButton></DateRangeButton>
        <Main>
          <WeeksHeader xs={1}></WeeksHeader>
          <Timetable xs={1}></Timetable>
        </Main>
        <RegisterButton />
      </Stack >
    </Provider>
  );
}