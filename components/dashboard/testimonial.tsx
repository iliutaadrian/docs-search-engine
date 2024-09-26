"use client";

export function Testimonial() {
  return (
    <section className="relative isolate overflow-hidden px-6 py-24 sm:py-32 lg:px-8">
      <div className="absolute inset-0 -z-10 opacity-20" />
      <div className="mx-auto max-w-2xl lg:max-w-4xl">
        <figure className="mt-10">
          <blockquote className="text-center  font-semibold leading-8 sm:text-xl sm:leading-9">
            <p>
              {"“"}Tube Mind Sync{"'"}s AI summaries have revolutionized the way
              I consume YouTube content. Now, I can quickly understand the key
              points of any video, saving me valuable time. Highly recommended!
              {"”"}
            </p>
          </blockquote>
          <figcaption className="mt-10">
            <img
              className="mx-auto h-10 w-10 rounded-full"
              src="https://images.unsplash.com/photo-1494790108377-be9c29b29330"
              alt=""
            />
            <div className="mt-4 flex items-center justify-center space-x-3 text-base">
              <div className="font-semibold">Sara Johnson</div>
              <svg
                viewBox="0 0 2 2"
                width={3}
                height={3}
                aria-hidden="true"
                className="fill-primary"
              >
                <circle cx={1} cy={1} r={1} />
              </svg>
              <div className="">Content Creator</div>
            </div>
          </figcaption>
        </figure>
      </div>
    </section>
  );
}
