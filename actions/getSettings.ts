import { BuildTable, SettingsTable, db } from "@/lib/db";
import { formatDate } from "@/lib/utils";
import { currentUser } from "@clerk/nextjs";
import { clear } from "console";
import { eq } from "drizzle-orm";

const getSettings = async () => {
  const user = await currentUser();

  if (!user?.id) {
    return null;
  }

  try {
    const settings = await db
      .select()
      .from(SettingsTable)
      .where(eq(SettingsTable.user_id, user.id));

    if (settings.length === 0) {
      return {
        settings: {
          imap: "imap.gmail.com",
          email: "",
          api_key: "",
          projects: [],
          bookmarks: [],
          last_deploy: ""
        }
      };
    }

    const buildsQuery = await db
      .select()
      .from(BuildTable)
      .where(eq(BuildTable.project, "test_develop"));
    const builds = buildsQuery.map((b) => ({ ...b, date: formatDate(b.date), dateBuild: b.date }));

    return {
      settings: settings[0],
      projects: settings[0].projects
        ? settings[0].projects.split(",").map((p) => ({ value: p, label: p }))
        : [],
      bookmarks: settings[0].bookmarks ? JSON.parse(settings[0].bookmarks) : [],
      builds
    };
  } catch (error: any) {
    console.log(error);
    return null;
  }
};

export default getSettings;
