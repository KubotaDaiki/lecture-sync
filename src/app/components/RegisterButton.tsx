import Button from '@mui/material/Button';
import CalendarMonthIcon from '@mui/icons-material/CalendarMonth'
import { useAtomValue, useAtom } from 'jotai'
import { scheduleAtom, startDateAtom } from "@/app/atoms"
import { useSession, useSupabaseClient } from "@supabase/auth-helpers-react";
import { AppName } from "@/app/constant";
import dayjs from 'dayjs';
import { useState } from "react";
import RegisterDialog from "@/app/components/RegisterDIalog"
import Cookies from 'js-cookie';

const times = [
  [dayjs("2021-01-01 09:10:00"), dayjs("2021-01-01 10:40:00")],
  [dayjs("2021-01-01 10:50:00"), dayjs("2021-01-01 12:20:00")],
  [dayjs("2021-01-01 13:15:00"), dayjs("2021-01-01 14:45:00")],
  [dayjs("2021-01-01 14:55:00"), dayjs("2021-01-01 16:25:00")],
  [dayjs("2021-01-01 16:35:00"), dayjs("2021-01-01 18:05:00")],
]

export default function RegisterButton() {
  const [open, setOpen] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [schedule, setSchedule] = useAtom(scheduleAtom)
  const startDate = useAtomValue(startDateAtom)
  const supabase = useSupabaseClient()

  async function getToken() {
    const { data, error } = await supabase.functions.invoke(
      'refreshGoogleToken',
      {
        method: 'POST',
        body: {
          providerRefreshToken: Cookies.get("oauth_provider_refresh_token"),
        },
      }
    )
    return data.access_token
  }

  async function getCalendarList(token: string) {
    const response = await fetch(
      "https://www.googleapis.com/calendar/v3/users/me/calendarList",
      {
        method: "GET",
        headers: {
          Authorization: "Bearer " + token,
        },
      }
    )
    return await response.json()
  }

  async function createAppCalender(token: string) {
    const response = await fetch(
      "https://www.googleapis.com/calendar/v3/calendars",
      {
        method: "POST",
        headers: {
          Authorization: "Bearer " + token,
        },
        body: JSON.stringify({
          summary: AppName,
        }),
      }
    )
    return await response.json()
  }

  async function createEvent(calenderId: string, token: string) {
    Object.keys(schedule).forEach(async (key) => {
      const period_idx = Number(key[0])
      const week_idx = Number(key[1]) - 1
      if ((schedule[key]["title"] == "") && (schedule[key]["place"] == "")) {
        return
      }
      const date = startDate.startOf("day").add(week_idx, "d")
      const startDatetime = date.add(times[period_idx][0].hour(), "h").add(times[period_idx][0].minute(), "m")
      const endDatetime = date.add(times[period_idx][1].hour(), "h").add(times[period_idx][1].minute(), "m")
      const event = {
        "summary": schedule[key]["title"],
        "start": {
          "dateTime": startDatetime.toISOString(),
          "timeZone": "Japan",
        },
        "end": {
          "dateTime": endDatetime.toISOString(),
          "timeZone": "Japan",
        },
        "location": schedule[key]["place"],
        "recurrence": ["RRULE:FREQ=WEEKLY"],
      }
      await fetch(
        `https://www.googleapis.com/calendar/v3/calendars/${calenderId}/events`,
        {
          method: "POST",
          headers: {
            Authorization: "Bearer " + token,
          },
          body: JSON.stringify(event),
        }
      )
    }
    );
  }

  async function getAppCalender(token: string) {
    const calenderList = await getCalendarList(token)
    const appCalender = calenderList.items.find(item => item.summary == AppName)
    if (appCalender === undefined) {
      return await createAppCalender(token)
    } else {
      return appCalender
    }
  }


  return (
    <>
      <Button
        variant="contained"
        startIcon={<CalendarMonthIcon />}
        size="large"
        onClick={() => setOpen(true)}
        sx={{ borderRadius: '35px' }}
      >
        カレンダーに登録
      </Button>
      <RegisterDialog
        open={open}
        isLoading={isLoading}
        handleCancel={() => setOpen(false)}
        handleOK={async () => {
          setIsLoading(true)

          const token = await getToken()
          const appCalender = await getAppCalender(token)
          await createEvent(appCalender.id, token)

          setSchedule({})
          setIsLoading(false)
          setOpen(false)
        }
        }>
      </RegisterDialog>
    </>
  )
}

