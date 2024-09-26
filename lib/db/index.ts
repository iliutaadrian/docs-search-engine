import { sql } from "@vercel/postgres";
import { drizzle } from "drizzle-orm/vercel-postgres";
import { integer, pgTable, serial, text, timestamp } from "drizzle-orm/pg-core";

// export const UserAPILimitTable = pgTable("user_api_limit", {
//   id: serial("id").primaryKey(),
//   user_id: text("userId").notNull().unique(),
//   limit: integer("limit").notNull(),
//   used: integer("used").notNull(),
//   stripeCustomerId: text("stripeCustomerId").notNull().unique(),
// });

// export const UserSubscriptionTable = pgTable("user_subscription", {
//   id: serial("id").primaryKey(),
//   user_id: text("userId").notNull().unique(),
//   stripeCustomerId: text("stripeCustomerId").notNull().unique(),
//   stripePriceId: text("stripePriceId").unique(),
//   stripeSubscriptionId: text("stripeSubscriptionId").notNull().unique(),
//   stripeCurrentPeriodEnd: timestamp("stripeCurrentPeriodEnd"),
// });

export const SettingsTable = pgTable("settings", {
  id: serial("id").primaryKey(),
  user_id: text("userId").notNull(),
  imap: text("imap").notNull(),
  email: text("email").notNull(),
  api_key: text("apiKey").notNull(),
  projects: text("projects").notNull(),
  bookmarks: text("bookmarks"),
  last_deploy: text("lastDeploy"),
});

export const BuildTable = pgTable("builds", {
  id: serial("id").primaryKey(),
  build: text("build").notNull(),
  project: text("project").notNull(),
  date: text("date").notNull(),
  link: text("link").notNull(),
  number_of_failures: text("number_of_failures").notNull(),
  subject: text("subject").notNull(),
});

export const TestTable = pgTable("tests", {
  id: serial("id").primaryKey(),
  build: text("build").notNull(),
  number: integer("number").notNull(),
  name: text("name").notNull(),
  content: text("content").notNull(),
});

export type Settings = typeof SettingsTable.$inferSelect;
export type Build = typeof BuildTable.$inferSelect;
export type Test = typeof TestTable.$inferSelect;

// Connect to Vercel Postgres
export const db = drizzle(sql);
