import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Star, ThumbsUp, MessageSquare } from 'lucide-react'
import Link from 'next/link'

interface ReviewCardProps {
  id: string
  userName: string
  userAvatar: string
  rating: number
  comment: string
  createdAt: string
  likes?: number
  isOwnReview?: boolean
}

export function ReviewCard({
  id,
  userName,
  userAvatar,
  rating,
  comment,
  createdAt,
  likes = 0,
  isOwnReview = false,
}: ReviewCardProps) {
  return (
    <Card>
      <CardContent className="pt-6">
        <div className="flex gap-4">
          <Link href={`/profile/${userName}`}>
            <Avatar className="h-12 w-12 ring-2 ring-border hover:ring-primary transition-all">
              <AvatarImage src={userAvatar || "/placeholder.svg"} alt={userName} />
              <AvatarFallback>{userName.slice(0, 2).toUpperCase()}</AvatarFallback>
            </Avatar>
          </Link>
          
          <div className="flex-1 space-y-3">
            <div className="flex items-start justify-between">
              <div>
                <Link href={`/profile/${userName}`} className="font-semibold hover:text-primary transition-colors">
                  {userName}
                </Link>
                <div className="flex items-center gap-2 mt-1">
                  <div className="flex items-center gap-1">
                    <Star className="h-4 w-4 fill-primary text-primary" />
                    <span className="font-bold text-lg">{rating}</span>
                    <span className="text-muted-foreground">/10</span>
                  </div>
                  <span className="text-sm text-muted-foreground">•</span>
                  <span className="text-sm text-muted-foreground">{createdAt}</span>
                </div>
              </div>
              {isOwnReview && (
                <Link href={`/reviews/${id}/edit`}>
                  <Button variant="outline" size="sm">
                    Editar
                  </Button>
                </Link>
              )}
            </div>
            
            <p className="text-foreground leading-relaxed">{comment}</p>
            
            <div className="flex items-center gap-2 pt-2">
              <Button variant="ghost" size="sm" className="gap-1">
                <ThumbsUp className="h-4 w-4" />
                <span>{likes}</span>
              </Button>
              <Button variant="ghost" size="sm" className="gap-1">
                <MessageSquare className="h-4 w-4" />
                Responder
              </Button>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
