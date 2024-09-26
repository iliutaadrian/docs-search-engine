import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function convertToAscii(value: string) {
  return value.replace(/[^\x00-\x7F]/g, "");
}

export function absoluteUrl(path: string) {
  return `${process.env.NEXT_PUBLIC_APP_URL}/${path}`;
}

function padZero(number: number) {
  return number < 10 ? '0' + number : number;
}

function formatToRO(date: Date) {
  const roFormatter = new Intl.DateTimeFormat('ro-RO', {
    timeZone: 'Europe/Bucharest',
    day: 'numeric',
    month: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  });

  // Format the date
  const parts = roFormatter.formatToParts(date);
  const day = parts.find(part => part.type === 'day')?.value;
  const month = parts.find(part => part.type === 'month')?.value;
  const hour = parts.find(part => part.type === 'hour')?.value;
  const minute = parts.find(part => part.type === 'minute')?.value;

  // Combine the formatted components into the desired format
  return `${day}.${month} ${hour}:${minute} RO`;
}

export function formatDate(date: string) {
  const d = new Date(date);
  const formattedDate = formatToRO(d);
  return formattedDate
}
