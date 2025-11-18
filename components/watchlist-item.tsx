'use client'

import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
} from '@/components/ui/dialog'
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
import { TrendingDown, TrendingUp, Edit2, Trash2, ExternalLink } from 'lucide-react'
import Image from 'next/image'
import Link from 'next/link'
import { useState } from 'react'

interface WatchlistItemProps {
  id: string
  gameId: string
  gameName: string
  gameCover: string
  currentPrice: number
  targetPrice: number
  lowestPrice: number
  addedDate: string
}

export function WatchlistItem({
  id,
  gameId,
  gameName,
  gameCover,
  currentPrice,
  targetPrice,
  lowestPrice,
  addedDate,
}: WatchlistItemProps) {
  const [newTargetPrice, setNewTargetPrice] = useState(targetPrice.toString())
  const isBelowTarget = currentPrice <= targetPrice
  const priceDifference = ((currentPrice - targetPrice) / targetPrice * 100).toFixed(0)

  const handleSavePrice = () => {
    console.log('Updated target price:', newTargetPrice)
  }

  const handleRemove = () => {
    console.log('Removed from watchlist:', id)
  }

  return (
    <Card className="hover:ring-2 hover:ring-primary/50 transition-all">
      <CardContent className="p-4">
        <div className="flex gap-4">
          <Link href={`/games/${gameId}`} className="shrink-0">
            <div className="relative w-20 h-28 rounded-md overflow-hidden bg-muted">
              <Image
                src={gameCover || "/placeholder.svg"}
                alt={gameName}
                fill
                className="object-cover"
              />
            </div>
          </Link>

          <div className="flex-1 min-w-0">
            <Link href={`/games/${gameId}`}>
              <h3 className="font-semibold text-lg mb-1 hover:text-primary transition-colors line-clamp-1">
                {gameName}
              </h3>
            </Link>
            
            <div className="flex flex-wrap gap-2 mb-3">
              <div className="flex items-center gap-1">
                <span className="text-sm text-muted-foreground">Preço atual:</span>
                <span className="font-bold text-lg">${currentPrice}</span>
              </div>
              <div className="flex items-center gap-1">
                <span className="text-sm text-muted-foreground">Meta:</span>
                <span className="font-semibold">${targetPrice}</span>
              </div>
            </div>

            <div className="mb-3">
              {isBelowTarget ? (
                <Badge className="bg-accent text-accent-foreground">
                  <TrendingDown className="h-3 w-3 mr-1" />
                  Abaixo da meta ({priceDifference}%)
                </Badge>
              ) : (
                <Badge variant="secondary">
                  <TrendingUp className="h-3 w-3 mr-1" />
                  Aguardando queda ({priceDifference}%)
                </Badge>
              )}
            </div>

            <div className="flex flex-wrap gap-2">
              <Link href={`/games/${gameId}`}>
                <Button size="sm" variant="outline" className="gap-1">
                  <ExternalLink className="h-3 w-3" />
                  Ver detalhes
                </Button>
              </Link>

              <Dialog>
                <DialogTrigger asChild>
                  <Button size="sm" variant="outline" className="gap-1">
                    <Edit2 className="h-3 w-3" />
                    Editar meta
                  </Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Editar preço alvo</DialogTitle>
                    <DialogDescription>{gameName}</DialogDescription>
                  </DialogHeader>
                  <div className="space-y-4 py-4">
                    <div className="space-y-2">
                      <Label htmlFor="target-price">Preço desejado</Label>
                      <Input
                        id="target-price"
                        type="number"
                        step="0.01"
                        value={newTargetPrice}
                        onChange={(e) => setNewTargetPrice(e.target.value)}
                      />
                    </div>
                    <div className="text-sm text-muted-foreground">
                      <p>Preço atual: ${currentPrice}</p>
                      <p>Menor preço histórico: ${lowestPrice}</p>
                    </div>
                  </div>
                  <DialogFooter>
                    <Button onClick={handleSavePrice}>Salvar</Button>
                  </DialogFooter>
                </DialogContent>
              </Dialog>

              <AlertDialog>
                <AlertDialogTrigger asChild>
                  <Button size="sm" variant="destructive" className="gap-1">
                    <Trash2 className="h-3 w-3" />
                    Remover
                  </Button>
                </AlertDialogTrigger>
                <AlertDialogContent>
                  <AlertDialogHeader>
                    <AlertDialogTitle>Remover do monitoramento?</AlertDialogTitle>
                    <AlertDialogDescription>
                      Você não receberá mais notificações quando o preço de {gameName} atingir sua meta.
                    </AlertDialogDescription>
                  </AlertDialogHeader>
                  <AlertDialogFooter>
                    <AlertDialogCancel>Cancelar</AlertDialogCancel>
                    <AlertDialogAction onClick={handleRemove} className="bg-destructive text-destructive-foreground hover:bg-destructive/90">
                      Remover
                    </AlertDialogAction>
                  </AlertDialogFooter>
                </AlertDialogContent>
              </AlertDialog>
            </div>

            <p className="text-xs text-muted-foreground mt-2">
              Adicionado {addedDate}
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
