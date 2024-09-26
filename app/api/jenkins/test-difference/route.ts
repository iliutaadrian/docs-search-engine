import { Build, Test, TestTable, db } from "@/lib/db";
import { currentUser } from "@clerk/nextjs";
import axios from "axios";
import { and, eq, or, sql } from "drizzle-orm";
import { NextResponse } from "next/server";

export async function POST(request: Request) {
  const user = await currentUser();
  if (!user) {
    return new NextResponse("Unauthorized", { status: 401 });
  }

  const body = await request.json();
  const { file_1, file_2 } = body;

  if (!file_1 || !file_2) {
    return new NextResponse("Missing parameters", { status: 400 });
  }

  try {
    const builds = [] as string[]

    // take last 10 builds
    for (let i = 0; i < 10; i++) {
      builds.push((parseInt(file_2) - i).toString());
    }

    const testsQuery = await db.execute(sql.raw(`
      SELECT *
      FROM tests
      WHERE build IN (
        ${builds.map((build) => `'${build}'`).join(",")}
      )
    `));
    const testResults: Test[] = testsQuery.rows as Test[];

    // Separate tests by file
    const testsFile1 = testResults.filter((test) => test.build === file_1);
    const testsFile2 = testResults.filter((test) => test.build === file_2);

    const testsFile1Names = testsFile1.map((test) => test.name);
    const testsFile2Names = testsFile2.map((test) => test.name);

    // Find differences
    const testDiff = testsFile2.filter((test) => !testsFile1Names.includes(test.name));
    const otherTests = testsFile2.filter((test) => testsFile1Names.includes(test.name));

    // Calculate occurrences and build info for tests in file_2
    const testOccurrences = testResults.reduce((acc, test) => {
      if (!acc[test.name]) {
        acc[test.name] = { count: 0, builds: [] as string[] };
      }
      acc[test.name].count += 1;
      acc[test.name].builds.push(`${test.build}#${test.number}`);
      return acc;
    }, {} as Record<string, { count: number; builds: string[] }>);

    const testDiffWithOccurrences = testDiff.map((test) => ({
      ...test,
      occurrences: testOccurrences[test.name]?.count || 0,
      occurrences_builds: testOccurrences[test.name]?.builds || [],
    })).sort((a, b) => a.occurrences - b.occurrences);

    const otherTestsWithOccurrences = otherTests.map((test) => ({
      ...test,
      occurrences: testOccurrences[test.name]?.count || 0,
      occurrences_builds: testOccurrences[test.name]?.builds || [],
    })).sort((a, b) => a.occurrences - b.occurrences);

    const result = {
      test_diff: testDiffWithOccurrences,
      other_tests: otherTestsWithOccurrences,
    };

    return new NextResponse(JSON.stringify(result), { status: 200 });
  } catch (error) {
    console.log(error);
    return new NextResponse("Something went wrong", { status: 500 });
  }
}
