"use client";

import { Menu } from "lucide-react";
import Link from "next/link";
import { UserButton } from "@clerk/nextjs";
import { ModeToggle } from "../mode-toggle";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "../ui/sheet";
import { Button } from "../ui/button";
import { useState } from "react";

interface Props {
  navigation: {
    name: string;
    href: string;
  }[];
}
export const MobileMenu = ({ navigation }: Props) => {
  const [open, setOpen] = useState(false);
  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger>
        <Menu />
      </SheetTrigger>
      <SheetContent className="border-none shadow-neonLight">
        <SheetHeader>
          <SheetTitle>Menu</SheetTitle>
        </SheetHeader>
        <div className="flex flex-col gap-5 items-center w-full mt-5 text-foreground">
          {navigation.length > 0 &&
            navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className="text-sm hover:text-primary"
                onClick={() => setOpen(false)}
              >
                {item.name}
              </Link>
            ))}
          <div className="flex flex-row justify-evenly items-center gap-5">
            <ModeToggle />
            <UserButton />
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
};
