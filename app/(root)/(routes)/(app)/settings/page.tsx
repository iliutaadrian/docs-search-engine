import getSettings from "@/actions/getSettings";
import { SettingsForm } from "@/components/settings/settings-form";
import { Separator } from "@/components/ui/separator";

async function Page() {
  const settings = await getSettings();
  if (!settings) {
    return null;
  }

  return (
    <div className="flex flex-col p-10 max-w-5xl mx-auto">
      <h2 className="text-2xl font-bold tracking-tight">Settings</h2>
      <p className="text-muted-foreground">Manage your account settings</p>
      <Separator className="bg-muted-foreground my-5" />
      <SettingsForm settings={settings} />
    </div>
  );
}

export default Page;
