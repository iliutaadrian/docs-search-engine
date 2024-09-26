import { CloudIcon } from "lucide-react";

export const Features = () => {
  const features = [
    {
      name: "Unlock Key Ideas",
      description:
        "Get the pivotal points and key ideas from any YouTube video, allowing you to grasp the essence of the content effortlessly.",
      icon: CloudIcon,
    },
    {
      name: "Language Translation",
      description:
        "Access translations of summaries in your preferred language with Eightify, eliminating language barriers and expanding your reach.",
      icon: CloudIcon,
    },
    {
      name: "Enhanced Navigation",
      description:
        "Navigate through videos with ease using summarized paragraphs with timestamps, enabling efficient content exploration.",
      icon: CloudIcon,
    },
    {
      name: "Time-Saving Solution",
      description:
        "Save valuable time by quickly understanding the essence of lengthy videos, empowering you to focus on what matters most.",
      icon: CloudIcon,
    },
  ];

  return (
    <div className=" py-24 sm:py-32">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl lg:text-center">
          <h2 className=" font-semibold leading-7 text-primary">Lean faster</h2>
          <p className="mt-2 text-3xl font-bold sm:text-4xl">
            Unlock the Power of Tube Mind Sync{"'"}s Cutting-Edge Features
          </p>
          <p className="mt-6 text-lg leading-8 text-muted-foreground">
            Explore the advanced features of Tube Mind Sync designed to
            revolutionize your YouTube video consumption experience. From
            accurate AI-generated summaries to seamless navigation and language
            translation, discover how our platform empowers you to grasp the
            essence of any video effortlessly.
          </p>
        </div>
        <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-4xl">
          <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-10 lg:max-w-none lg:grid-cols-2 lg:gap-y-16">
            {features.map((feature) => (
              <div key={feature.name} className="relative pl-16">
                <dt className="text-base font-semibold leading-7 ">
                  <div className="absolute left-0 top-0 flex h-10 w-10 items-center justify-center rounded-lg bg-primary">
                    <feature.icon
                      className="h-6 w-6 text-white"
                      aria-hidden="true"
                    />
                  </div>
                  {feature.name}
                </dt>
                <dd className="mt-2 text-base leading-7 text-muted-foreground">
                  {feature.description}
                </dd>
              </div>
            ))}
          </dl>
        </div>
      </div>
    </div>
  );
};
