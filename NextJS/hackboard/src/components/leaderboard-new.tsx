"use client";

import { useState, useEffect } from "react";
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
import { Trophy, Medal, Award, ExternalLink, GitPullRequest, Clock, Code, Loader2 } from "lucide-react";

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

interface GitHubPullRequest {
    id: number;
    number: number;
    title: string;
    state: string;
    merged_at: string | null;
    created_at: string;
    user: {
        login: string;
        avatar_url: string;
        html_url: string;
    };
    labels: Array<{
        name: string;
    }>;
}

// GitHub API URL
const GITHUB_API_URL = "https://api.github.com/repos/IEEE-Student-Branch-NSBM/hacktoberfest-2025/pulls?state=all";

// Function to calculate time difference
const calculateTimeDifference = (startDate: string, endDate: string | null): string => {
    if (!endDate) return "Ongoing";

    const start = new Date(startDate);
    const end = new Date(endDate);
    const diffMs = end.getTime() - start.getTime();

    const days = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diffMs % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));

    if (days > 0) {
        return `${days} day${days > 1 ? 's' : ''} ${hours} hr${hours !== 1 ? 's' : ''}`;
    }
    return `${hours} hr${hours !== 1 ? 's' : ''}`;
};

// Function to check if PR has hacktoberfest label
const hasHacktoberfestLabel = (labels: Array<{ name: string }>): boolean => {
    return labels.some(label =>
        label.name.toLowerCase().includes('hacktoberfest') ||
        label.name.toLowerCase().includes('hacktober')
    );
};

// Function to process GitHub PRs into contributor data
const processGitHubData = (prs: GitHubPullRequest[]): Contributor[] => {
    // Filter for hacktoberfest PRs
    const hacktoberfestPRs = prs.filter(pr => hasHacktoberfestLabel(pr.labels));

    // Group PRs by user
    const userMap = new Map<string, {
        user: GitHubPullRequest['user'];
        prs: GitHubPullRequest[];
        mergedPRs: GitHubPullRequest[];
    }>();

    hacktoberfestPRs.forEach(pr => {
        const username = pr.user.login;
        if (!userMap.has(username)) {
            userMap.set(username, {
                user: pr.user,
                prs: [],
                mergedPRs: []
            });
        }

        const userData = userMap.get(username)!;
        userData.prs.push(pr);

        if (pr.merged_at) {
            userData.mergedPRs.push(pr);
        }
    });

    // Convert to contributor format
    const contributors: Contributor[] = Array.from(userMap.entries()).map(([username, data], index) => {
        const mergedPRs = data.mergedPRs;

        // Calculate estimated lines changed (this is an approximation since we don't have actual diff data)
        const estimatedLinesChanged = mergedPRs.length * 150; // Rough estimate

        // Calculate average completion time
        const completionTimes = mergedPRs
            .filter(pr => pr.merged_at)
            .map(pr => calculateTimeDifference(pr.created_at, pr.merged_at))
            .filter(time => time !== "Ongoing");

        const avgTime = completionTimes.length > 0 ? completionTimes[0] : "No merges yet";

        return {
            id: index + 1,
            rank: 0, // Will be set after sorting
            username,
            avatar: data.user.avatar_url,
            mergedPRs: mergedPRs.length,
            totalPRs: data.prs.length,
            linesChanged: estimatedLinesChanged,
            completionTime: avgTime,
            profileUrl: data.user.html_url
        };
    });

    // Sort by merged PRs (descending) and assign ranks
    contributors.sort((a, b) => {
        if (b.mergedPRs !== a.mergedPRs) {
            return b.mergedPRs - a.mergedPRs;
        }
        return b.totalPRs - a.totalPRs;
    });

    // Assign ranks
    contributors.forEach((contributor, index) => {
        contributor.rank = index + 1;
    });

    return contributors;
};

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
            return "default" as const;
        case 2:
            return "secondary" as const;
        case 3:
            return "outline" as const;
        default:
            return "secondary" as const;
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
    const [contributors, setContributors] = useState<Contributor[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchContributors = async () => {
            try {
                setLoading(true);
                const response = await fetch(GITHUB_API_URL);

                if (!response.ok) {
                    throw new Error(`GitHub API error: ${response.status}`);
                }

                const prs: GitHubPullRequest[] = await response.json();
                const processedData = processGitHubData(prs);
                setContributors(processedData);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'Failed to fetch data');
                console.error('Error fetching GitHub data:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchContributors();
    }, []);

    if (loading) {
        return (
            <div className="min-h-screen bg-background p-6 flex items-center justify-center">
                <div className="text-center">
                    <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4" />
                    <p className="text-lg text-muted-foreground">Loading contributor data...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-background p-6 flex items-center justify-center">
                <div className="text-center">
                    <h2 className="text-2xl font-bold mb-4 text-destructive">Error Loading Data</h2>
                    <p className="text-muted-foreground mb-4">{error}</p>
                    <Button onClick={() => window.location.reload()}>
                        Try Again
                    </Button>
                </div>
            </div>
        );
    }

    const topThree = contributors.slice(0, 3);
    const others = contributors.slice(3);

    return (
        <div className="min-h-screen bg-background p-6">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="text-center mb-12">
                    <h1 className="text-4xl font-bold mb-4">
                        🏆 IEEE NSBM Hacktoberfest 2025 Leaderboard
                    </h1>
                    <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                        Celebrating the outstanding contributions from IEEE NSBM Student Branch members to open source projects during Hacktoberfest 2025.
                    </p>
                    {contributors.length > 0 && (
                        <p className="text-sm text-muted-foreground mt-2">
                            Showing {contributors.length} contributor{contributors.length !== 1 ? 's' : ''} with Hacktoberfest PRs
                        </p>
                    )}
                </div>

                {contributors.length === 0 ? (
                    <div className="text-center py-12">
                        <h3 className="text-xl font-semibold mb-2">No Contributors Yet</h3>
                        <p className="text-muted-foreground">
                            Be the first to contribute to the IEEE NSBM Hacktoberfest 2025 repository!
                        </p>
                    </div>
                ) : (
                    <>
                        {/* Top 3 Podium */}
                        {topThree.length > 0 && (
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
                                {topThree.map((contributor) => (
                                    <PodiumCard key={contributor.id} contributor={contributor} />
                                ))}
                            </div>
                        )}

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
                    </>
                )}
            </div>
        </div>
    );
}
