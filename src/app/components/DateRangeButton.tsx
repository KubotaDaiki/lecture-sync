import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { startDateAtom } from "@/app/atoms"
import { useAtom } from 'jotai'
import 'dayjs/locale/ja';

export default function BasicDatePicker() {
    const [startDate, setStartDate] = useAtom(startDateAtom)

    const isMonday = (date) => {
        const day = date.day();

        return day !== 1;
    };

    return (
        <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale="ja">
            <DatePicker
                label="予定開始日"
                sx={{ maxWidth: "200px" }}
                onChange={(value) => { setStartDate(value!) }}
                value={startDate}
                shouldDisableDate={isMonday}
            />
        </LocalizationProvider>
    );
}