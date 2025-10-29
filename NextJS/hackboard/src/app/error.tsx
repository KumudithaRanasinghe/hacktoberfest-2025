'use client'

import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { RefreshCcw, ArrowLeft } from 'lucide-react'

export default function Error({
    error,
    reset,
}: {
    error: Error & { digest?: string }
    reset: () => void
}) {
    return (
        <div className="flex min-h-[70vh] flex-col items-center justify-center gap-4">
            <div className="space-y-4 text-center">
                <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl">Something went wrong!</h1>
                <p className="text-muted-foreground">
                    An unexpected error occurred. Please try again or return to the homepage.
                </p>
            </div>
            <div className="flex gap-4 mt-4">
                <Button onClick={() => reset()} variant="secondary">
                    <RefreshCcw className="mr-2 h-4 w-4" />
                    Try Again
                </Button>
                <Button asChild>
                    <Link href="/">
                        <ArrowLeft className="mr-2 h-4 w-4" />
                        Back to Home
                    </Link>
                </Button>
            </div>
        </div>
    )
}
