import Link from 'next/link'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Star, TrendingDown } from 'lucide-react'
import Image from 'next/image'

interface GameCardProps {
  id: string
  name: string
  coverImage: string
  averageRating: number
  currentPrice?: number
  priceDown?: boolean
  categories?: string[]
}

export function GameCard({
  id,
  name,
  coverImage,
  averageRating,
  currentPrice,
  priceDown,
  categories = [],
}: GameCardProps) {
  return (
    <Link href={`/games/${id}`}>
      <Card className="group overflow-hidden hover:ring-2 hover:ring-primary transition-all duration-200">
        <div className="relative aspect-[3/4] overflow-hidden bg-muted">
          <Image
            src={coverImage || "/placeholder.svg"}
            alt={name}
            fill
            className="object-cover group-hover:scale-105 transition-transform duration-300"
          />
          {priceDown && currentPrice && (
            <div className="absolute top-2 right-2 bg-accent text-accent-foreground px-2 py-1 rounded-md text-xs font-semibold flex items-center gap-1">
              <TrendingDown className="h-3 w-3" />
              ${currentPrice}
            </div>
          )}
        </div>
        <CardContent className="p-4">
          <h3 className="font-semibold text-base line-clamp-1 mb-2">{name}</h3>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-1">
              <Star className="h-4 w-4 fill-primary text-primary" />
              <span className="font-medium text-sm">{averageRating.toFixed(1)}</span>
            </div>
            {currentPrice && !priceDown && (
              <span className="text-sm text-muted-foreground">${currentPrice}</span>
            )}
          </div>
          {categories.length > 0 && (
            <div className="flex flex-wrap gap-1 mt-2">
              {categories.slice(0, 2).map((category) => (
                <Badge key={category} variant="secondary" className="text-xs">
                  {category}
                </Badge>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </Link>
  )
}
