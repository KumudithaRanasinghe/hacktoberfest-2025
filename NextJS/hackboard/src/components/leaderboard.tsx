"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import { Trophy, Medal, Award, ExternalLink, GitPullRequest, Clock, Code } from "lucide-react";

interface Contributor {
    id: number;
    rank: number;
    username: string;
    avatar: string;
    mergedPRs: number;
    totalPRs: number;
    linesChanged: number;
    completionTime: string;
    profileUrl: string;
}

const mockData: Contributor[] = [
    {
        id: 1,
        rank: 1,
        username: "alexsmith",
        avatar: "https://github.com/alexsmith.png",
        mergedPRs: 8,
        totalPRs: 8,
        linesChanged: 1250,
        completionTime: "1 day 6 hrs",
        profileUrl: "https://github.com/alexsmith"
    },
    {
        id: 2,
        rank: 2,
        username: "sarahdev",
        avatar: "https://github.com/sarahdev.png",
        mergedPRs: 7,
        totalPRs: 8,
        linesChanged: 980,
        completionTime: "1 day 18 hrs",
        profileUrl: "https://github.com/sarahdev"
    },
    {
        id: 3,
        rank: 3,
        username: "mikecoder",
        avatar: "https://github.com/mikecoder.png",
        mergedPRs: 6,
        totalPRs: 6,
        linesChanged: 745,
        completionTime: "2 days 4 hrs",
        profileUrl: "https://github.com/mikecoder"
    },
    {
        id: 4,
        rank: 4,
        username: "janeoss",
        avatar: "https://github.com/janeoss.png",
        mergedPRs: 5,
        totalPRs: 6,
        linesChanged: 620,
        completionTime: "2 days 12 hrs",
        profileUrl: "https://github.com/janeoss"
    },
    {
        id: 5,
        rank: 5,
        username: "devjohn",
        avatar: "https://github.com/devjohn.png",
        mergedPRs: 4,
        totalPRs: 5,
        linesChanged: 485,
        completionTime: "3 days 8 hrs",
        profileUrl: "https://github.com/devjohn"
    },
    {
        id: 6,
        rank: 6,
        username: "codecat",
        avatar: "https://github.com/codecat.png",
        mergedPRs: 4,
        totalPRs: 6,
        linesChanged: 410,
        completionTime: "4 days 2 hrs",
        profileUrl: "https://github.com/codecat"
    },
    {
        id: 7,
        rank: 7,
        username: "hackergirl",
        avatar: "https://github.com/hackergirl.png",
        mergedPRs: 3,
        totalPRs: 4,
        linesChanged: 350,
        completionTime: "3 days 16 hrs",
        profileUrl: "https://github.com/hackergirl"
    },
    {
        id: 8,
        rank: 8,
        username: "pythonista",
        avatar: "https://github.com/pythonista.png",
        mergedPRs: 3,
        totalPRs: 5,
        linesChanged: 295,
        completionTime: "5 days 1 hr",
        profileUrl: "https://github.com/pythonista"
    }
];

const getRankIcon = (rank: number) => {
    switch (rank) {
        case 1:
            return <Trophy className="h-6 w-6" />;
        case 2:
            return <Medal className="h-6 w-6" />;
        case 3:
            return <Award className="h-6 w-6" />;
        default:
            return <span className="text-lg font-bold text-muted-foreground">#{rank}</span>;
    }
};

const getRankBadgeVariant = (rank: number) => {
    switch (rank) {
        case 1:
            return "default";
        case 2:
            return "secondary";
        case 3:
            return "outline";
        default:
            return "secondary";
    }
};

const PodiumCard = ({ contributor }: { contributor: Contributor }) => {
    const completionPercentage = (contributor.mergedPRs / contributor.totalPRs) * 100;

    return (
        <Card className="relative overflow-hidden">
            <CardHeader className="text-center pb-4">
                <div className="flex justify-center mb-4">
                    <Badge variant={getRankBadgeVariant(contributor.rank)} className="px-3 py-1 text-sm font-bold">
                        {getRankIcon(contributor.rank)}
                        <span className="ml-2">#{contributor.rank}</span>
                    </Badge>
                </div>

                <div className="relative mb-4">
                    <Avatar className="h-20 w-20 mx-auto">
                        <AvatarImage src={contributor.avatar} alt={contributor.username} />
                        <AvatarFallback className="text-xl font-bold">
                            {contributor.username.slice(0, 2).toUpperCase()}
                        </AvatarFallback>
                    </Avatar>
                </div>

                <Button
                    variant="link"
                    className="p-0 h-auto font-bold text-lg"
                    onClick={() => window.open(contributor.profileUrl, '_blank')}
                >
                    @{contributor.username}
                    <ExternalLink className="h-4 w-4 ml-1" />
                </Button>
            </CardHeader>

            <CardContent className="pt-0">
                <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
                    <div className="flex items-center justify-center space-x-2">
                        <GitPullRequest className="h-4 w-4" />
                        <span className="font-semibold">{contributor.mergedPRs} PRs</span>
                    </div>
                    <div className="flex items-center justify-center space-x-2">
                        <Code className="h-4 w-4" />
                        <span className="font-semibold">{contributor.linesChanged} lines</span>
                    </div>
                </div>

                <div className="flex items-center justify-center space-x-2 mb-4 text-sm text-muted-foreground">
                    <Clock className="h-4 w-4" />
                    <span>{contributor.completionTime}</span>
                </div>

                <div className="border-t mb-4" />

                <div>
                    <div className="flex justify-between text-xs text-muted-foreground mb-2">
                        <span>Progress</span>
                        <span>{contributor.mergedPRs}/{contributor.totalPRs} PRs</span>
                    </div>
                    <Progress value={completionPercentage} className="h-2" />
                </div>
            </CardContent>
        </Card>
    );
};

export default function Leaderboard() {
    const topThree = mockData.slice(0, 3);
    const others = mockData.slice(3);

    return (
        <div className="min-h-screen bg-background p-6">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="text-center mb-12">
                    <h1 className="text-4xl font-bold mb-4">
                        IEEE NSBM Hacktoberfest 2025 Leaderboard
                    </h1>
                    <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                        Celebrating the outstanding contributions from IEEE NSBM Student Branch members to open source projects during Hacktoberfest 2025.
                    </p>
                </div>

                {/* Top 3 Podium */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
                    {topThree.map((contributor) => (
                        <PodiumCard key={contributor.id} contributor={contributor} />
                    ))}
                </div>

                {/* Other Contributors Table */}
                {others.length > 0 && (
                    <Card>
                        <CardHeader>
                            <CardTitle className="text-2xl">Other Contributors</CardTitle>
                            <p className="text-muted-foreground">Keep up the great work!</p>
                        </CardHeader>
                        <CardContent className="p-0">
                            <Table>
                                <TableHeader>
                                    <TableRow className="hover:bg-transparent">
                                        <TableHead className="w-16">Rank</TableHead>
                                        <TableHead>Contributor</TableHead>
                                        <TableHead className="text-center">Merged PRs</TableHead>
                                        <TableHead className="text-center">Lines Changed</TableHead>
                                        <TableHead className="text-center">Completion Time</TableHead>
                                        <TableHead className="text-center">Progress</TableHead>
                                        <TableHead className="w-16"></TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {others.map((contributor) => {
                                        const completionPercentage = (contributor.mergedPRs / contributor.totalPRs) * 100;

                                        return (
                                            <TableRow key={contributor.id} className="hover:bg-muted/50 transition-colors">
                                                <TableCell>
                                                    <div className="flex items-center justify-center">
                                                        {getRankIcon(contributor.rank)}
                                                    </div>
                                                </TableCell>

                                                <TableCell>
                                                    <div className="flex items-center space-x-3">
                                                        <Avatar className="h-10 w-10">
                                                            <AvatarImage src={contributor.avatar} alt={contributor.username} />
                                                            <AvatarFallback>
                                                                {contributor.username.slice(0, 2).toUpperCase()}
                                                            </AvatarFallback>
                                                        </Avatar>
                                                        <Button
                                                            variant="link"
                                                            className="p-0 h-auto font-medium"
                                                            onClick={() => window.open(contributor.profileUrl, '_blank')}
                                                        >
                                                            @{contributor.username}
                                                        </Button>
                                                    </div>
                                                </TableCell>

                                                <TableCell className="text-center">
                                                    <div className="flex items-center justify-center space-x-2">
                                                        <GitPullRequest className="h-4 w-4" />
                                                        <span className="font-semibold">{contributor.mergedPRs}</span>
                                                    </div>
                                                </TableCell>

                                                <TableCell className="text-center">
                                                    <div className="flex items-center justify-center space-x-2">
                                                        <Code className="h-4 w-4" />
                                                        <span className="font-semibold">{contributor.linesChanged}</span>
                                                    </div>
                                                </TableCell>

                                                <TableCell className="text-center">
                                                    <div className="flex items-center justify-center space-x-2 text-muted-foreground">
                                                        <Clock className="h-4 w-4" />
                                                        <span className="text-sm">{contributor.completionTime}</span>
                                                    </div>
                                                </TableCell>

                                                <TableCell className="text-center">
                                                    <div className="w-full max-w-24 mx-auto">
                                                        <div className="flex justify-between text-xs text-muted-foreground mb-1">
                                                            <span>{contributor.mergedPRs}</span>
                                                            <span>{contributor.totalPRs}</span>
                                                        </div>
                                                        <Progress value={completionPercentage} className="h-2" />
                                                    </div>
                                                </TableCell>

                                                <TableCell>
                                                    <Button
                                                        variant="ghost"
                                                        size="sm"
                                                        onClick={() => window.open(contributor.profileUrl, '_blank')}
                                                    >
                                                        <ExternalLink className="h-4 w-4" />
                                                    </Button>
                                                </TableCell>
                                            </TableRow>
                                        );
                                    })}
                                </TableBody>
                            </Table>
                        </CardContent>
                    </Card>
                )}
            </div>
        </div>
    );
}
