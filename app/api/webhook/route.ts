// import { headers } from "next/headers";
// import { NextResponse } from "next/server";
// import Stripe from "stripe";
//
// import { stripe } from "@/lib/stripe/stripe";
// import { buyCredits } from "@/lib/stripe/api-limits";
//
export async function POST(req: Request) {
  //   const body = await req.text();
  //   const signature = headers().get("Stripe-Signature") as string;
  //
  //   let event: Stripe.Event;
  //
  //   try {
  //     event = stripe.webhooks.constructEvent(
  //       body,
  //       signature,
  //       process.env.STRIPE_WEBHOOK_SECRET!,
  //     );
  //   } catch (error: any) {
  //     return new NextResponse(`Webhook Error: ${error.message}`, { status: 400 });
  //   }
  //
  //   if (event.type === "checkout.session.completed") {
  //     const paymentIntent = event.data.object;
  //     const userID = paymentIntent?.metadata?.userId;
  //     if (!userID) {
  //       return new NextResponse("Webhook Error", { status: 400 });
  //     }
  //
  //     switch (paymentIntent.amount_total) {
  //       case 700:
  //         await buyCredits(userID, 100, "");
  //         break;
  //       case 2000:
  //         await buyCredits(userID, 1000, "");
  //         break;
  //     }
  //   }
  //
  //   return new NextResponse(null, { status: 200 });
}
