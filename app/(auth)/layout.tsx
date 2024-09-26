export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div
      className={
        "flex flex-col min-h-full justify-center items-center bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-primary/40 to-background"
      }
    >
      <h1 className="text-3xl font-medium py-5">
        {/* Create/Register for free to get started! */}
      </h1>
      {children}
    </div>
  );
}
