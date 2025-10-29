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
import { Trophy, Medal, Award, ExternalLink, GitPullRequest, Clock, Code, Loader2, Users, TrendingUp, GitBranch, FileCode } from "lucide-react";

interface Contributor {
    id: number;
    rank: number;
    username: string;
    avatar: string;
    mergedPRs: number;
    totalPRs: number;
    additions: number;
    deletions: number;
    commits: number;
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

interface GitHubPullRequestDetail {
    additions: number;
    deletions: number;
    commits: number;
}

const GITHUB_API_URL = "https://api.github.com/repos/IEEE-Student-Branch-NSBM/hacktoberfest-2025/pulls?state=all";


const fetchPRDetails = async (prNumber: number): Promise<GitHubPullRequestDetail | null> => {
    try {
        const response = await fetch(`https://api.github.com/repos/IEEE-Student-Branch-NSBM/hacktoberfest-2025/pulls/${prNumber}`);
        if (!response.ok) {
            console.warn(`Failed to fetch details for PR #${prNumber}`);
            return null;
        }
        const data = await response.json();
        return {
            additions: data.additions || 0,
            deletions: data.deletions || 0,
            commits: data.commits || 0
        };
    } catch (error) {
        console.warn(`Error fetching PR #${prNumber} details:`, error);
        return null;
    }
};

const hasHacktoberfestLabel = (labels: Array<{ name: string }>): boolean => {
    return labels.some(label =>
        label.name.toLowerCase().includes('hacktoberfest') ||
        label.name.toLowerCase().includes('hacktober')
    );
};

const processGitHubData = async (prs: GitHubPullRequest[]): Promise<Contributor[]> => {
    const hacktoberfestPRs = prs.filter(pr => hasHacktoberfestLabel(pr.labels));

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

    const contributors: Contributor[] = [];
    let index = 0;

    for (const [username, data] of userMap.entries()) {
        const mergedPRs = data.mergedPRs;

        const prDetails = await Promise.all(
            data.prs.map(pr => fetchPRDetails(pr.number))
        );

        let totalAdditions = 0;
        let totalDeletions = 0;
        let totalCommits = 0;

        prDetails.forEach(detail => {
            if (detail) {
                totalAdditions += detail.additions;
                totalDeletions += detail.deletions;
                totalCommits += detail.commits;
            }
        });

        contributors.push({
            id: index + 1,
            rank: 0,
            username,
            avatar: data.user.avatar_url,
            mergedPRs: mergedPRs.length,
            totalPRs: data.prs.length,
            additions: totalAdditions,
            deletions: totalDeletions,
            commits: totalCommits,
            profileUrl: data.user.html_url
        });

        index++;
    }

    contributors.sort((a, b) => {
        if (b.mergedPRs !== a.mergedPRs) {
            return b.mergedPRs - a.mergedPRs;
        }
        return b.totalPRs - a.totalPRs;
    });

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
    const completionPercentage = (contributor.mergedPRs / 6) * 100;

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
                    className="p-0 h-auto font-bold text-lg text-blue-600 hover:text-blue-700"
                    onClick={() => window.open(contributor.profileUrl, '_blank')}
                >
                    @{contributor.username}
                    <ExternalLink className="h-4 w-4 ml-1" />
                </Button>
            </CardHeader>

            <CardContent className="pt-0">
                <div className="grid grid-cols-3 gap-4 mb-4 text-sm">
                    <div className="flex items-center justify-center space-x-2">
                        <GitPullRequest className="h-4 w-4" />
                        <span className="font-semibold">{contributor.mergedPRs} PRs</span>
                    </div>
                    <div className="flex items-center justify-center space-x-2">
                        <span className="text-green-600 font-semibold">+{contributor.additions}</span>
                    </div>
                    <div className="flex items-center justify-center space-x-2">
                        <span className="text-red-600 font-semibold">-{contributor.deletions}</span>
                    </div>
                </div>

                <div className="flex items-center justify-center space-x-2 mb-4 text-sm text-muted-foreground">
                    <Code className="h-4 w-4" />
                    <span>{contributor.commits} commits</span>
                </div>

                <div className="border-t mb-4" />

                <div>
                    <div className="flex justify-between text-xs text-muted-foreground mb-2">
                        <span>Progress</span>
                        <span>{contributor.mergedPRs}/6 PRs</span>
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
    const [searchQuery, setSearchQuery] = useState("");
    const [minMergedPRs, setMinMergedPRs] = useState<number>(0);

    useEffect(() => {
        const fetchContributors = async () => {
            try {
                setLoading(true);
                const response = await fetch(GITHUB_API_URL);

                if (!response.ok) {
                    throw new Error(`GitHub API error: ${response.status}`);
                }

                const prs: GitHubPullRequest[] = await response.json();
                const processedData = await processGitHubData(prs);
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

    // Initialize theme from localStorage or system preference
    useEffect(() => {
        try {
            const stored = localStorage.getItem("theme");
            let initial: "light" | "dark" = "light";
            if (stored === "light" || stored === "dark") {
                initial = stored;
            } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                initial = "dark";
            }
            setTheme(initial);
            document.documentElement.classList.toggle('dark', initial === 'dark');
        } catch {}
    }, []);

    const toggleTheme = () => {
        const next = theme === 'dark' ? 'light' : 'dark';
        setTheme(next);
        document.documentElement.classList.toggle('dark', next === 'dark');
        try { localStorage.setItem('theme', next); } catch {}
    };

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
                    <Button onClick={() => window.location.reload()} className="bg-blue-600 hover:bg-blue-700 text-white">
                        Try Again
                    </Button>
                </div>
            </div>
        );
    }

    const normalizedQuery = searchQuery.trim().toLowerCase();
    const filteredContributors = contributors.filter((c) => {
        const matchesQuery = normalizedQuery === "" || c.username.toLowerCase().includes(normalizedQuery);
        const meetsMinMerged = c.mergedPRs >= minMergedPRs;
        return matchesQuery && meetsMinMerged;
    });

    // Calculate statistics
    const totalContributors = contributors.length;
    const totalMergedPRs = contributors.reduce((sum, c) => sum + c.mergedPRs, 0);
    const totalAdditions = contributors.reduce((sum, c) => sum + c.additions, 0);
    const totalDeletions = contributors.reduce((sum, c) => sum + c.deletions, 0);
    const totalCommits = contributors.reduce((sum, c) => sum + c.commits, 0);
    const averageMergedPRs = totalContributors > 0 ? (totalMergedPRs / totalContributors).toFixed(1) : '0';
    const topContributor = contributors.length > 0 ? contributors[0] : null;

    const topThree = filteredContributors.slice(0, 3);
    const others = filteredContributors.slice(3);

    return (
        <div className="min-h-screen bg-background p-6">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="text-center mb-8">
                    <h1 className="text-4xl font-bold mb-4">
                        🏆 IEEE NSBM Hacktoberfest 2025 Leaderboard
                    </h1>
                    <div className="flex items-center justify-center gap-3 mb-3">
                        <Button
                            variant="outline"
                            onClick={toggleTheme}
                            className="flex items-center gap-2"
                            title={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
                        >
                            {theme === 'dark' ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
                            <span className="text-sm">{theme === 'dark' ? 'Light mode' : 'Dark mode'}</span>
                        </Button>
                    </div>
                    <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                        Celebrating the outstanding contributions from IEEE NSBM Student Branch members to open source projects during Hacktoberfest 2025.
                    </p>
                    {filteredContributors.length > 0 && (
                        <p className="text-sm text-muted-foreground mt-2">
                            Showing {filteredContributors.length} contributor{filteredContributors.length !== 1 ? 's' : ''} with Hacktoberfest PRs
                        </p>
                    )}
                </div>

                {/* Filters */}
                <div className="mb-12">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="col-span-1">
                            <label className="block text-sm font-medium text-muted-foreground mb-1">Search by username</label>
                            <input
                                type="text"
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                placeholder="e.g. octocat"
                                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                        </div>
                        <div className="col-span-1">
                            <label className="block text-sm font-medium text-muted-foreground mb-1">Min merged PRs</label>
                            <select
                                value={minMergedPRs}
                                onChange={(e) => setMinMergedPRs(Number(e.target.value))}
                                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                            >
                                <option value={0}>0</option>
                                <option value={1}>1</option>
                                <option value={2}>2</option>
                                <option value={3}>3</option>
                                <option value={4}>4</option>
                                <option value={5}>5</option>
                                <option value={6}>6</option>
                            </select>
                        </div>
                        <div className="col-span-1 flex items-end">
                            <Button
                                className="bg-blue-600 hover:bg-blue-700 text-white w-full"
                                onClick={() => {
                                    setSearchQuery("");
                                    setMinMergedPRs(0);
                                }}
                            >
                                Clear filters
                            </Button>
                        </div>
                    </div>
                </div>

                {/* Statistics Dashboard */}
                {contributors.length > 0 && (
                    <div className="mb-12">
                        <h2 className="text-2xl font-bold mb-6 text-center">📊 Project Statistics</h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                            {/* Total Contributors */}
                            <Card className="border-blue-200">
                                <CardHeader className="pb-3">
                                    <div className="flex items-center justify-between">
                                        <CardTitle className="text-sm font-medium text-muted-foreground">Total Contributors</CardTitle>
                                        <Users className="h-5 w-5 text-blue-600" />
                                    </div>
                                </CardHeader>
                                <CardContent>
                                    <div className="text-3xl font-bold text-blue-600">{totalContributors}</div>
                                    <p className="text-xs text-muted-foreground mt-1">Active developers</p>
                                </CardContent>
                            </Card>

                            {/* Total Merged PRs */}
                            <Card className="border-green-200">
                                <CardHeader className="pb-3">
                                    <div className="flex items-center justify-between">
                                        <CardTitle className="text-sm font-medium text-muted-foreground">Merged PRs</CardTitle>
                                        <GitBranch className="h-5 w-5 text-green-600" />
                                    </div>
                                </CardHeader>
                                <CardContent>
                                    <div className="text-3xl font-bold text-green-600">{totalMergedPRs}</div>
                                    <p className="text-xs text-muted-foreground mt-1">Avg {averageMergedPRs} per contributor</p>
                                </CardContent>
                            </Card>

                            {/* Code Changes */}
                            <Card className="border-purple-200">
                                <CardHeader className="pb-3">
                                    <div className="flex items-center justify-between">
                                        <CardTitle className="text-sm font-medium text-muted-foreground">Code Changes</CardTitle>
                                        <FileCode className="h-5 w-5 text-purple-600" />
                                    </div>
                                </CardHeader>
                                <CardContent>
                                    <div className="text-3xl font-bold text-purple-600">
                                        {totalAdditions > 0 ? '+' : ''}{totalAdditions.toLocaleString()}
                                    </div>
                                    <p className="text-xs text-muted-foreground mt-1">
                                        {totalDeletions > 0 && `-${totalDeletions.toLocaleString()} deletions`}
                                    </p>
                                </CardContent>
                            </Card>

                            {/* Total Commits */}
                            <Card className="border-orange-200">
                                <CardHeader className="pb-3">
                                    <div className="flex items-center justify-between">
                                        <CardTitle className="text-sm font-medium text-muted-foreground">Total Commits</CardTitle>
                                        <TrendingUp className="h-5 w-5 text-orange-600" />
                                    </div>
                                </CardHeader>
                                <CardContent>
                                    <div className="text-3xl font-bold text-orange-600">{totalCommits.toLocaleString()}</div>
                                    <p className="text-xs text-muted-foreground mt-1">
                                        {topContributor && `Top: @${topContributor.username}`}
                                    </p>
                                </CardContent>
                            </Card>
                        </div>
                    </div>
                )}

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
                                                <TableHead className="w-16 text-red-600 font-semibold">Rank</TableHead>
                                                <TableHead className="text-red-600 font-semibold">Contributor</TableHead>
                                                <TableHead className="text-center text-red-600 font-semibold">Merged PRs</TableHead>
                                                <TableHead className="text-center text-red-600 font-semibold">Additions</TableHead>
                                                <TableHead className="text-center text-red-600 font-semibold">Deletions</TableHead>
                                                <TableHead className="text-center text-red-600 font-semibold">Commits</TableHead>
                                                <TableHead className="text-center text-red-600 font-semibold">Progress</TableHead>
                                                <TableHead className="w-16"></TableHead>
                                            </TableRow>
                                        </TableHeader>
                                        <TableBody>
                                            {others.map((contributor) => {
                                                const completionPercentage = (contributor.mergedPRs / 6) * 100;

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
                                                                    className="p-0 h-auto font-medium text-blue-600 hover:text-blue-700"
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
                                                                <span className="text-green-600 font-semibold">+{contributor.additions}</span>
                                                            </div>
                                                        </TableCell>

                                                        <TableCell className="text-center">
                                                            <div className="flex items-center justify-center space-x-2">
                                                                <span className="text-red-600 font-semibold">-{contributor.deletions}</span>
                                                            </div>
                                                        </TableCell>

                                                        <TableCell className="text-center">
                                                            <div className="flex items-center justify-center space-x-2">
                                                                <Code className="h-4 w-4" />
                                                                <span className="font-semibold">{contributor.commits}</span>
                                                            </div>
                                                        </TableCell>

                                                        <TableCell className="text-center">
                                                            <div className="w-full max-w-24 mx-auto">
                                                                <div className="flex justify-between text-xs text-muted-foreground mb-1">
                                                                    <span>{contributor.mergedPRs}</span>
                                                                    <span>6</span>
                                                                </div>
                                                                <Progress value={completionPercentage} className="h-2" />
                                                            </div>
                                                        </TableCell>

                                                        <TableCell>
                                                            <Button
                                                                variant="ghost"
                                                                size="sm"
                                                                className="text-blue-600 hover:text-blue-700 hover:bg-blue-50"
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
