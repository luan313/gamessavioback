import { NavHeader } from '@/components/nav-header'
import { PriceHistoryChart } from '@/components/price-history-chart'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { TrendingDown, TrendingUp, ExternalLink } from 'lucide-react'
import Image from 'next/image'
import Link from 'next/link'

// Mock data
const gameData = {
  id: '1',
  name: 'The Last of Us Part II',
  coverImage: '/the-last-of-us-game-cover.jpg',
  currentPrice: 39.99,
  lowestPrice: 29.99,
  highestPrice: 59.99,
  averagePrice: 45.50,
}

const priceHistory = [
  { date: '01/07', price: 59.99, store: 'Steam' },
  { date: '15/07', price: 59.99, store: 'Steam' },
  { date: '01/08', price: 54.99, store: 'Epic' },
  { date: '15/08', price: 54.99, store: 'Steam' },
  { date: '01/09', price: 49.99, store: 'GOG' },
  { date: '15/09', price: 49.99, store: 'Steam' },
  { date: '01/10', price: 44.99, store: 'Epic' },
  { date: '15/10', price: 44.99, store: 'Steam' },
  { date: '01/11', price: 39.99, store: 'GOG' },
  { date: '15/11', price: 39.99, store: 'Steam' },
  { date: '01/12', price: 34.99, store: 'Epic' },
  { date: '15/12', price: 29.99, store: 'Steam' },
  { date: '01/01', price: 39.99, store: 'GOG' },
  { date: '15/01', price: 39.99, store: 'Steam' },
]

const storeHistory = [
  { store: 'Steam', price: 39.99, lastUpdate: 'há 2 dias', isLowest: true },
  { store: 'Epic Games Store', price: 44.99, lastUpdate: 'há 1 semana', isLowest: false },
  { store: 'GOG', price: 42.99, lastUpdate: 'há 3 dias', isLowest: false },
  { store: 'PlayStation Store', price: 49.99, lastUpdate: 'há 5 dias', isLowest: false },
]

export default function PriceHistoryPage() {
  return (
    <div className="min-h-screen bg-background">
      <NavHeader />
      
      <main className="container mx-auto px-4 py-8">
        <Link href={`/games/${gameData.id}`} className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground mb-6 transition-colors">
          ← Voltar para o jogo
        </Link>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Charts */}
          <div className="lg:col-span-2 space-y-6">
            <div className="flex gap-4">
              <div className="relative w-32 aspect-[3/4] rounded-lg overflow-hidden bg-muted shrink-0">
                <Image
                  src={gameData.coverImage || "/placeholder.svg"}
                  alt={gameData.name}
                  fill
                  className="object-cover"
                />
              </div>
              <div>
                <h1 className="text-3xl font-bold mb-2">{gameData.name}</h1>
                <p className="text-muted-foreground mb-4">
                  Histórico completo de preços e comparação entre lojas
                </p>
                <div className="flex items-center gap-2">
                  <span className="text-3xl font-bold">${gameData.currentPrice}</span>
                  <Badge variant="secondary">Preço atual</Badge>
                </div>
              </div>
            </div>

            <PriceHistoryChart data={priceHistory} />

            {/* Price Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Card>
                <CardHeader className="pb-3">
                  <CardDescription>Menor Preço</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center gap-2">
                    <TrendingDown className="h-5 w-5 text-accent" />
                    <span className="text-2xl font-bold text-accent">${gameData.lowestPrice}</span>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-3">
                  <CardDescription>Maior Preço</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center gap-2">
                    <TrendingUp className="h-5 w-5 text-muted-foreground" />
                    <span className="text-2xl font-bold">${gameData.highestPrice}</span>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-3">
                  <CardDescription>Preço Médio</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">${gameData.averagePrice}</div>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Right Column - Store Prices */}
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Preços por Loja</CardTitle>
                <CardDescription>Comparação em tempo real</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {storeHistory.map((item) => (
                  <div
                    key={item.store}
                    className="flex items-center justify-between p-3 rounded-lg border border-border hover:border-primary transition-colors"
                  >
                    <div className="flex-1">
                      <div className="font-semibold mb-1">{item.store}</div>
                      <div className="text-xs text-muted-foreground">
                        Atualizado {item.lastUpdate}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="flex items-center gap-2">
                        <span className="text-xl font-bold">${item.price}</span>
                        {item.isLowest && (
                          <Badge className="bg-accent text-accent-foreground">
                            Melhor
                          </Badge>
                        )}
                      </div>
                      <Button size="sm" variant="ghost" className="mt-1 h-7 gap-1">
                        <ExternalLink className="h-3 w-3" />
                        Ver oferta
                      </Button>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>

            <Card className="mt-6">
              <CardHeader>
                <CardTitle>Dicas de Economia</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2 text-sm">
                <p className="text-muted-foreground">
                  • O menor preço foi de ${gameData.lowestPrice} em Dezembro
                </p>
                <p className="text-muted-foreground">
                  • Economia de {((gameData.highestPrice - gameData.currentPrice) / gameData.highestPrice * 100).toFixed(0)}% vs. o preço mais alto
                </p>
                <p className="text-muted-foreground">
                  • Adicione à watchlist para ser notificado de ofertas
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  )
}
