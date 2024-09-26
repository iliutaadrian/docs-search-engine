import { Build, BuildTable, SettingsTable, Test, TestTable, db } from "@/lib/db";
import { currentUser } from "@clerk/nextjs";
import axios from "axios";
import { clear, debug } from "console";
import { eq } from "drizzle-orm";
import { NextResponse } from "next/server";

export async function GET(
  request: Request,
) {

  try {
    const userSettings = await db
      .select()
      .from(SettingsTable)

    if (userSettings.length === 0) {
      return new NextResponse(
        "No settings found. Make sure to add your email details and project name in settings.",
        { status: 400 },
      );
    }

    const projects = userSettings[0].projects.split(",");

    let previousBuilds = await db
      .select()
      .from(BuildTable)
      .where(eq(BuildTable.project, projects[0]));
    const builds = previousBuilds.map((item) => item.build);

    const data = await axios
      .get(`${process.env.PYTHON_URL}/fetch_data`, {
        params: {
          imap_server: "imap.gmail.com",
          email_address: userSettings[0].email,
          password: userSettings[0].api_key,
          project: projects[0],
        },
      })
      .then((res) => {
        return res.data.data;
      });

    for (const item of data) {
      if (!builds.includes(item.build)) {
        await db.insert(BuildTable).values({
          project: projects[0],
          build: item.build,
          date: item.date,
          link: item.link,
          number_of_failures: item.number_of_failures,
          subject: item.subject,
        })

        const data = await axios
          .get(`${process.env.PYTHON_URL}/get_test`, {
            params: {
              file: item.link,
            },
          })
          .then((res) => {
            return res.data;
          });

        data.forEach(async (t: Test) => {
          await db
            .insert(TestTable)
            .values({
              build: item.build,
              number: t.number,
              name: t.name,
              content: t.content,
            });
        })
      }
    }

    previousBuilds = await db
      .select()
      .from(BuildTable)
      .where(eq(BuildTable.project, projects[0]));

    return new NextResponse(
      JSON.stringify(
        previousBuilds.slice(previousBuilds.length - 10, previousBuilds.length),
      ),
      {
        status: 200,
      },
    );

  } catch (error) {
    console.log(error);
    return new NextResponse("Something went wrong", { status: 500 });
  }
}

