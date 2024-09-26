"use client";
import React, { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import Image from "next/image";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

function Page() {
  const [roTime, setRoTime] = useState(new Date().toLocaleString());
  const [usTime, setUsTime] = useState(
    new Date().toLocaleString("en-US", { timeZone: "America/New_York" }),
  );

  useEffect(() => {
    // Update time every second
    const intervalId = setInterval(() => {
      setRoTime(new Date().toLocaleString());
      setUsTime(
        new Date().toLocaleString("en-US", { timeZone: "America/New_York" }),
      );
    }, 1000);

    // Clean up interval on unmount
    return () => clearInterval(intervalId);
  }, []); // Empty dependency array ensures effect runs only once on mount

  return (
    <div className="flex w-full min-h-[calc(100vh_-_theme(spacing.16))] flex-1 flex-col gap-4 bg-muted/40 p-4 md:gap-8 md:p-10">
      <Image
        className="blur-sm -z-10"
        src="/background.jpg"
        blurDataURL="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mPkso6pBwACGgEie2Im0gAAAABJRU5ErkJggg=="
        placeholder="blur"
        layout="fill"
        objectFit="cover"
        objectPosition="center"
        alt="Background image"
      />
      <Card className="bg-gray-500/50 border-0 p-2 flex">
        <CardContent>
          <div>
            <div className="text-xl">RO Time</div>
            <div className="text-xl">{roTime}</div>
            <div className="text-xl">US Time</div>
            <div className="text-xl">{usTime}</div>
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Store Name</CardTitle>
          <CardDescription>
            Used to identify your store in the marketplace.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form>
            <Input placeholder="Store Name" />
            <Button>Save</Button>
          </form>
        </CardContent>
        <CardFooter className="border-t px-6 py-4"></CardFooter>
      </Card>
    </div>
  );
}

export default Page;
