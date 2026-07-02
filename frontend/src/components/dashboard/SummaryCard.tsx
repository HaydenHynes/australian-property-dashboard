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
}

export function SummaryCard({ title, value, caption }: SummaryCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-sm font-medium text-muted-foreground">
          {title}
        </CardTitle>
      </CardHeader>

      <CardContent>
        <p className="text-3xl font-bold">{value}</p>
        <p className="mt-2 text-sm text-muted-foreground">{caption}</p>
      </CardContent>
    </Card>
  );
}