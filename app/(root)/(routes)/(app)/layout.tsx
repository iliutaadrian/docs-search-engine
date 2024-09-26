import { Navbar } from "@/components/menu/navbar";

export default function RoutesLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="h-screen flex flex-col justify-between">
      <Navbar />
      <div className={" pt-10 flex flex-col items-center"}>
        <div className={" h-full w-full"}>{children}</div>
      </div>
    </div>
  );
}
