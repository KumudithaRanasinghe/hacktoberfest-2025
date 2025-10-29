import Link from 'next/link'

export function Footer() {
    return (
        <footer className="w-full border-t py-3 text-center text-sm text-muted-foreground">
            <div className="container flex items-center justify-center space-x-2">
                <p>© {new Date().getFullYear()} IEEE NSBM.</p>
                <span>•</span>
                <p>
                    Dev by{' '}
                    <Link
                        href="https://github.com/dizzpy"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="hover:underline"
                    >
                        @dizzpy
                    </Link>
                </p>
            </div>
        </footer>
    )
}
