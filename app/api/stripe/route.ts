import { stripe } from "@/lib/stripe/stripe";
import { absoluteUrl } from "@/lib/utils";
import { auth, currentUser } from "@clerk/nextjs";
import { NextResponse } from "next/server";

const summaryURL = absoluteUrl("/summary");
const priceURL = absoluteUrl("/#pricing");

export async function POST(request: Request) {
  try {
    const { userId } = auth();
    const user = await currentUser();

    if (!userId || !user) {
      return new NextResponse("Unauthorized", { status: 401 });
    }

    const body = await request.json();
    const { name, price, facilities_yes } = body;

    // const userSubscriptionQuery = await db
    //   .select()
    //   .from(UserSubscriptionTable)
    //   .where(eq(UserSubscriptionTable.user_id, userId));
    // const userSubscription = userSubscriptionQuery[0];
    //
    // if (userSubscription && userSubscription.stripeCustomerId) {
    //   const stripeSession = await stripe.billingPortal.sessions.create({
    //     customer: userSubscription.stripeCustomerId,
    //     return_url: summaryURL,
    //   });
    //
    //   return new NextResponse(JSON.stringify({ url: stripeSession.url }));
    // }

    const stripeSession = await stripe.checkout.sessions.create({
      success_url: summaryURL,
      cancel_url: priceURL,
      payment_method_types: ["card"],
      mode: "payment", // or subscription
      billing_address_collection: "auto",
      customer_email: user.emailAddresses[0].emailAddress,
      line_items: [
        {
          price_data: {
            currency: "USD",
            product_data: {
              name: name,
              description: facilities_yes.join(",\n"),
            },
            unit_amount: price * 100,
          },
          quantity: 1,
        },
      ],
      metadata: {
        userId,
        test: 1,
      },
    });

    return new NextResponse(JSON.stringify({ url: stripeSession.url }));
  } catch (error) {
    console.log("[STRIPE_ERROR]", error);
    return new NextResponse("Internal Error", { status: 500 });
  }
}
