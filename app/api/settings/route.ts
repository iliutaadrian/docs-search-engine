import { SettingsTable, db } from "@/lib/db";
import { currentUser } from "@clerk/nextjs";
import { eq } from "drizzle-orm";
import { NextResponse } from "next/server";

export async function POST(request: Request) {
  const user = await currentUser();
  if (!user) {
    return new NextResponse("Unauthorized", { status: 401 });
  }

  const body = await request.json();
  const { imap, email, api_key, projects, bookmarks } = body;

  if (!imap || !email || !api_key) {
    return new NextResponse("Missing required fields", { status: 400 });
  }

  try {
    const userSettings = await db
      .select()
      .from(SettingsTable)
      .where(eq(SettingsTable.user_id, user.id));

    if (userSettings.length === 0) {
      await db.insert(SettingsTable).values({
        user_id: user.id,
        imap,
        email,
        api_key,
        projects: projects ? projects : "",
        bookmarks: bookmarks ? JSON.stringify(bookmarks) : "",
      });
    } else {
      let projectsEdited = "";
      if (projects !== "") {
        projectsEdited = projects
          .split(",")
          .filter((project: string) => project !== "")
          .join(",");
      }

      await db
        .update(SettingsTable)
        .set({
          imap,
          email,
          api_key,
          projects: projectsEdited,
          bookmarks: JSON.stringify(bookmarks),
        })
        .where(eq(SettingsTable.user_id, user.id));
    }
  } catch (error) {
    console.log(error);
    return new NextResponse("Something went wrong", { status: 500 });
  }

  return new NextResponse("OK", { status: 200 });
}
