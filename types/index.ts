import { Build, Settings } from "@/lib/db";

export type UserClerk = {
  id: string;
  username: string | null | undefined;
  createdAt: number | null | undefined;
};

export type ReportJenkins = {
  build: string;
  date: string;
  link: string;
  number_of_failures: string;
  subject: string;
};

export type ComboList = {
  label: string;
  value: string;
};

export type Usage = {
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
};

export type SettingsFull =
  {
    settings: Settings
    project: ComboList[];
    bookmarks: { name: string; url: string }[];
    builds: BuildFull[]
  }

export type BuildFull = Build & { dateBuild: Date }

export const MAX_FREE_CREDITS = 5;
