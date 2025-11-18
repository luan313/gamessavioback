'use client'

import { NavHeader } from '@/components/nav-header'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Star } from 'lucide-react'
import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function ReviewGamePage() {
  const router = useRouter()
  const [rating, setRating] = useState(0)
  const [hoveredRating, setHoveredRating] = useState(0)
  const [comment, setComment] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Here you would normally submit the review to your backend
    console.log({ rating, comment })
    router.push('/games/1') // Redirect back to game page
  }

  return (
    <div className="min-h-screen bg-background">
      <NavHeader />
      
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          <Card>
            <CardHeader>
              <CardTitle className="text-2xl">Avaliar The Last of Us Part II</CardTitle>
              <CardDescription>
                Compartilhe sua opinião sobre este jogo com a comunidade
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Rating */}
                <div className="space-y-3">
                  <Label className="text-base">Sua nota</Label>
                  <div className="flex items-center gap-2">
                    {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((value) => (
                      <button
                        key={value}
                        type="button"
                        onClick={() => setRating(value)}
                        onMouseEnter={() => setHoveredRating(value)}
                        onMouseLeave={() => setHoveredRating(0)}
                        className="group relative"
                      >
                        <Star
                          className={`h-8 w-8 transition-all ${
                            value <= (hoveredRating || rating)
                              ? 'fill-primary text-primary scale-110'
                              : 'text-muted-foreground'
                          }`}
                        />
                        <span className="absolute -bottom-6 left-1/2 -translate-x-1/2 text-xs font-medium opacity-0 group-hover:opacity-100 transition-opacity">
                          {value}
                        </span>
                      </button>
                    ))}
                  </div>
                  {rating > 0 && (
                    <p className="text-sm text-muted-foreground">
                      Você avaliou com {rating}/10
                    </p>
                  )}
                </div>
                
                {/* Comment */}
                <div className="space-y-2">
                  <Label htmlFor="comment" className="text-base">
                    Seu comentário
                  </Label>
                  <Textarea
                    id="comment"
                    placeholder="Conte o que você achou do jogo... (opcional)"
                    className="min-h-[200px] resize-none"
                    value={comment}
                    onChange={(e) => setComment(e.target.value)}
                  />
                  <p className="text-xs text-muted-foreground">
                    {comment.length} caracteres
                  </p>
                </div>
                
                <div className="flex gap-3">
                  <Button
                    type="submit"
                    size="lg"
                    disabled={rating === 0}
                    className="flex-1"
                  >
                    Publicar Avaliação
                  </Button>
                  <Button
                    type="button"
                    size="lg"
                    variant="outline"
                    onClick={() => router.back()}
                  >
                    Cancelar
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
