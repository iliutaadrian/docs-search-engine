"use client";
import { cn } from "@/lib/utils";
import { Button } from "../ui/button";
import { CheckIcon, XIcon } from "lucide-react";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

export function Faq() {
  const faqs = [
    {
      question: "What is Tube Mind Sync?",
      answer:
        "Tube Mind Sync is a revolutionary tool that harnesses advanced AI technology to summarize YouTube videos quickly and effectively, providing concise summaries for easy understanding.",
    },
    {
      question: "Is Tube Mind Sync compatible with mobile devices?",
      answer:
        "Yes, Tube Mind Sync is fully compatible with mobile devices. Whether you're using an iOS device or browsing on Chrome or Safari, you can easily access our summarization tool on the go.",
    },
    {
      question: "How does Tube Mind Sync summarize videos?",
      answer:
        "Tube Mind Sync leverages cutting-edge AI algorithms, including OpenAI GPT, to analyze and condense the key points of YouTube videos. Our technology ensures accurate and comprehensive summaries.",
    },
    {
      question: "Can Tube Mind Sync be used for podcasts and news content?",
      answer:
        "Currently, Tube Mind Sync focuses on summarizing YouTube videos. However, many podcasts and news segments are available on YouTube and can be summarized using our tool.",
    },
    {
      question:
        "Does Tube Mind Sync support video summarization in multiple languages?",
      answer:
        "Yes, Tube Mind Sync supports video summarization in various languages. With translations available in over 40 languages, language barriers are no longer an issue.",
    },
    {
      question: "Can Tube Mind Sync handle lengthy videos?",
      answer:
        "Absolutely. Tube Mind Sync can summarize even lengthy videos, making it suitable for content of any duration. While there are technical limitations, our tool is highly efficient for summarizing extensive content.",
    },
    {
      question: "Can I use Tube Mind Sync to summarize my own videos?",
      answer:
        "Yes, you can. Tube Mind Sync allows you to upload your own unlisted videos on YouTube and summarize them effortlessly using our AI-powered tool.",
    },
  ];

  return (
    <div
      className="md:max-w-5xl mx-auto py-10 flex flex-col md:flex-row"
      id="faq"
    >
      <div className="basis-1/2">
        <h1 className="text-2xl md:text-4xl text-primary text-center">
          Frequently Asked Questions
        </h1>
        <h1 className=" font-medium text-center">
          Have another question? Contact me on Twitter or by email.
        </h1>
      </div>
      <div className="basis-1/2 px-10">
        {faqs.map((faq, index) => (
          <Accordion key={index} type="single" collapsible>
            <AccordionItem value={faq.question} className="my-5">
              <AccordionTrigger>{faq.question}</AccordionTrigger>
              <AccordionContent className="text-muted-foreground">
                {faq.answer}
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        ))}
      </div>
    </div>
  );
}
