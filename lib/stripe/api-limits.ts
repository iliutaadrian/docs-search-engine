// import { MAX_FREE_CREDITS } from "@/types";
// import { UserAPILimitTable, db } from "../db";
// import { eq } from "drizzle-orm";
// import { auth } from "@clerk/nextjs";
//
// export const increaseUserApiLimit = async () => {
//   const { userId } = auth();
//
//   if (!userId) {
//     return;
//   }
//
//   const userApiLimits = await db
//     .select()
//     .from(UserAPILimitTable)
//     .where(eq(UserAPILimitTable.user_id, userId));
//
//   if (userApiLimits.length === 0) {
//     await db.insert(UserAPILimitTable).values({
//       user_id: userId,
//       limit: MAX_FREE_CREDITS,
//       used: 1,
//       stripeCustomerId: "",
//     });
//   } else {
//     await db
//       .update(UserAPILimitTable)
//       .set({ used: userApiLimits[0].used + 1 })
//       .where(eq(UserAPILimitTable.user_id, userId));
//   }
// };
//
// export const buyCredits = async (
//   userId: string,
//   credits: number,
//   stripeCustomerId: string,
// ) => {
//   const userApiLimits = await db
//     .select()
//     .from(UserAPILimitTable)
//     .where(eq(UserAPILimitTable.user_id, userId));
//
//   if (userApiLimits.length === 0) {
//     await db.insert(UserAPILimitTable).values({
//       user_id: userId,
//       limit: credits,
//       used: 0,
//       stripeCustomerId: stripeCustomerId,
//     });
//   } else {
//     await db
//       .update(UserAPILimitTable)
//       .set({
//         limit: credits + userApiLimits[0].limit,
//         stripeCustomerId: stripeCustomerId,
//       })
//       .where(eq(UserAPILimitTable.user_id, userId));
//   }
// };
//
// export const checkUserApiLimit = async () => {
//   const { userId } = auth();
//   if (!userId) {
//     return;
//   }
//
//   const userApiLimits = await db
//     .select()
//     .from(UserAPILimitTable)
//     .where(eq(UserAPILimitTable.user_id, userId));
//
//   if (userApiLimits.length === 0) {
//     return true;
//   }
//
//   return userApiLimits[0].used < userApiLimits[0].limit;
// };
//
// export const getUserApiLimit = async () => {
//   const { userId } = auth();
//   if (!userId) {
//     return;
//   }
//
//   const userApiLimits = await db
//     .select()
//     .from(UserAPILimitTable)
//     .where(eq(UserAPILimitTable.user_id, userId));
//
//   if (userApiLimits.length === 0) {
//     return [0, MAX_FREE_CREDITS];
//   }
//
//   return [userApiLimits[0].used, userApiLimits[0].limit];
// };
