"use client";

import * as React from "react";
import { Check, ChevronsUpDown } from "lucide-react";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { ComboList } from "@/types";

interface Props {
  disabled?: boolean;
  list: ComboList[];
  setValue: (value: string) => void;
  text: string;
  value: string;
}
export function Combobox({ list, text, value, setValue, disabled }: Props) {
  const [open, setOpen] = React.useState(false);

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          disabled={disabled}
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className="w-full py-7 justify-between"
        >
          {value
            ? list.find((item) => item.value.toLocaleLowerCase() === value)
                ?.label
            : text}
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[500px] max-h-[300px] overflow-y-scroll p-0">
        <Command>
          <CommandInput placeholder={text} />
          <CommandEmpty>No item found.</CommandEmpty>
          <CommandGroup>
            {list.length === 0 && <CommandItem>No item found.</CommandItem>}
            {list.map((item) => (
              <CommandItem
                key={item.value}
                value={item.value}
                onSelect={(currentValue) => {
                  setValue(currentValue);
                  setOpen(false);
                }}
              >
                <Check
                  className={cn(
                    "mr-2 h-4 w-4",
                    value === item.value ? "opacity-100" : "opacity-0",
                  )}
                />
                {item.label}
              </CommandItem>
            ))}
          </CommandGroup>
        </Command>
      </PopoverContent>
    </Popover>
  );
}
