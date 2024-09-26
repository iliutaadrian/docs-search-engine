import { SettingsTable, db } from "@/lib/db";
import { currentUser } from "@clerk/nextjs";
import { eq } from "drizzle-orm";
import { NextResponse } from "next/server";

export async function PUT(request: Request, { params }: { params: { settingsId: string } }) {
  const user = await currentUser();
  if (!user) {
    return new NextResponse("Unauthorized", { status: 401 });
  }

  const body = await request.json();
  const { settings } = body;

  if (!settings) {
    return new NextResponse("Missing required fields", { status: 400 });
  }

  try {
    await db
      .update(SettingsTable)
      .set({
        last_deploy: settings.last_deploy,
      })
      .where(eq(SettingsTable.id, settings.id));
  } catch (error) {
    console.log(error);
    return new NextResponse("Something went wrong", { status: 500 });
  }

  return new NextResponse("OK", { status: 200 });
}
