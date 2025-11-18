'use client'

import { NavHeader } from '@/components/nav-header'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Star, Trash2 } from 'lucide-react'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog'

export default function EditReviewPage() {
  const router = useRouter()
  // Mock existing review data
  const [rating, setRating] = useState(8)
  const [hoveredRating, setHoveredRating] = useState(0)
  const [comment, setComment] = useState('Jogo incrível com gráficos de última geração e história emocionante.')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log({ rating, comment })
    router.push('/profile') // Redirect to profile
  }

  const handleDelete = () => {
    // Handle review deletion
    console.log('Review deleted')
    router.push('/profile')
  }

  return (
    <div className="min-h-screen bg-background">
      <NavHeader />
      
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          <Card>
            <CardHeader>
              <CardTitle className="text-2xl">Editar Avaliação</CardTitle>
              <CardDescription>
                The Last of Us Part II
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
                    placeholder="Conte o que você achou do jogo..."
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
                    Salvar Alterações
                  </Button>
                  <Button
                    type="button"
                    size="lg"
                    variant="outline"
                    onClick={() => router.back()}
                  >
                    Cancelar
                  </Button>
                  
                  <AlertDialog>
                    <AlertDialogTrigger asChild>
                      <Button
                        type="button"
                        size="lg"
                        variant="destructive"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </AlertDialogTrigger>
                    <AlertDialogContent>
                      <AlertDialogHeader>
                        <AlertDialogTitle>Excluir avaliação?</AlertDialogTitle>
                        <AlertDialogDescription>
                          Esta ação não pode ser desfeita. Sua avaliação será permanentemente removida.
                        </AlertDialogDescription>
                      </AlertDialogHeader>
                      <AlertDialogFooter>
                        <AlertDialogCancel>Cancelar</AlertDialogCancel>
                        <AlertDialogAction onClick={handleDelete} className="bg-destructive text-destructive-foreground hover:bg-destructive/90">
                          Excluir
                        </AlertDialogAction>
                      </AlertDialogFooter>
                    </AlertDialogContent>
                  </AlertDialog>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
