import type { LucideIcon } from "lucide-react";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

interface SummaryCardProps {
  title: string;
  value: string;
  caption: string;
  icon: LucideIcon;
}

export function SummaryCard({
  title,
  value,
  caption,
  icon: Icon,
}: SummaryCardProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">
          {title}
        </CardTitle>

        <Icon className="h-5 w-5 text-sky-400" />
      </CardHeader>

      <CardContent>
        <p className="text-3xl font-bold">{value}</p>
        <p className="mt-2 text-sm text-muted-foreground">{caption}</p>
      </CardContent>
    </Card>
  );
}