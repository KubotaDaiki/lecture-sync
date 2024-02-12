import { atom } from 'jotai'
import dayjs from 'dayjs'

export const scheduleAtom = atom({})

export const startDateAtom = atom(dayjs())