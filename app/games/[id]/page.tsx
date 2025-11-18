import { NavHeader } from '@/components/nav-header'
import { ReviewCard } from '@/components/review-card'
import { PriceHistoryChart } from '@/components/price-history-chart'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Star, DollarSign, TrendingDown, Bell, ExternalLink } from 'lucide-react'
import Image from 'next/image'
import Link from 'next/link'

// Mock data
const gameData = {
  id: '1',
  name: 'The Last of Us Part II',
  description: 'The Last of Us Part II é um jogo eletrônico de ação-aventura desenvolvido pela Naughty Dog e publicado pela Sony Interactive Entertainment. É o segundo jogo da franquia e foi lançado em 19 de junho de 2020 exclusivamente para PlayStation 4. A história se passa cinco anos após os eventos do primeiro jogo e segue Ellie em uma jornada de vingança.',
  coverImage: '/the-last-of-us-game-cover.jpg',
  averageRating: 9.5,
  totalReviews: 1247,
  currentPrice: 39.99,
  lowestPrice: 29.99,
  categories: ['Ação', 'Aventura', 'Survival Horror'],
  releaseDate: '19 de junho de 2020',
  developer: 'Naughty Dog',
  publisher: 'Sony Interactive Entertainment',
}

const priceHistory = [
  { date: '01/10', price: 59.99, store: 'Steam' },
  { date: '15/10', price: 54.99, store: 'Steam' },
  { date: '01/11', price: 49.99, store: 'Epic' },
  { date: '15/11', price: 44.99, store: 'Steam' },
  { date: '01/12', price: 39.99, store: 'GOG' },
  { date: '15/12', price: 39.99, store: 'Steam' },
  { date: '01/01', price: 39.99, store: 'Epic' },
]

const reviews = [
  {
    id: '1',
    userName: 'João Silva',
    userAvatar: '/diverse-user-avatars.png',
    rating: 10,
    comment: 'Uma obra-prima absoluta. A narrativa é envolvente, os personagens são profundos e o gameplay é impecável. Naughty Dog conseguiu superar todas as expectativas com este jogo.',
    createdAt: 'há 2 dias',
    likes: 24,
  },
  {
    id: '2',
    userName: 'Maria Santos',
    userAvatar: '/diverse-user-avatars.png',
    rating: 9,
    comment: 'Jogo incrível com gráficos de última geração e história emocionante. Apenas alguns problemas de ritmo no meio do jogo, mas nada que tire o brilho desta experiência.',
    createdAt: 'há 5 dias',
    likes: 18,
  },
  {
    id: '3',
    userName: 'Pedro Costa',
    userAvatar: '/diverse-user-avatars.png',
    rating: 8,
    comment: 'Tecnicamente perfeito e com uma história corajosa. Não agradou todos, mas é impossível negar a qualidade do trabalho da Naughty Dog.',
    createdAt: 'há 1 semana',
    likes: 12,
  },
]

export default function GameDetailsPage() {
  return (
    <div className="min-h-screen bg-background">
      <NavHeader />
      
      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Game Info */}
          <div className="lg:col-span-2 space-y-6">
            {/* Game Header */}
            <div className="flex flex-col md:flex-row gap-6">
              <div className="relative w-full md:w-64 aspect-[3/4] rounded-lg overflow-hidden bg-muted">
                <Image
                  src={gameData.coverImage || "/placeholder.svg"}
                  alt={gameData.name}
                  fill
                  className="object-cover"
                />
              </div>
              
              <div className="flex-1 space-y-4">
                <div>
                  <h1 className="text-3xl md:text-4xl font-bold mb-2">{gameData.name}</h1>
                  <div className="flex flex-wrap gap-2 mb-3">
                    {gameData.categories.map((category) => (
                      <Badge key={category} variant="secondary">
                        {category}
                      </Badge>
                    ))}
                  </div>
                  <div className="flex items-center gap-4 text-sm text-muted-foreground">
                    <span>{gameData.developer}</span>
                    <span>•</span>
                    <span>{gameData.releaseDate}</span>
                  </div>
                </div>
                
                <div className="flex items-center gap-6">
                  <div className="flex items-center gap-2">
                    <Star className="h-6 w-6 fill-primary text-primary" />
                    <div>
                      <div className="text-2xl font-bold">{gameData.averageRating}</div>
                      <div className="text-xs text-muted-foreground">{gameData.totalReviews} avaliações</div>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-2">
                    <DollarSign className="h-6 w-6 text-accent" />
                    <div>
                      <div className="text-2xl font-bold">${gameData.currentPrice}</div>
                      <div className="text-xs text-muted-foreground">Preço atual</div>
                    </div>
                  </div>
                </div>
                
                <p className="text-muted-foreground leading-relaxed">
                  {gameData.description}
                </p>
                
                <div className="flex flex-wrap gap-3">
                  <Link href={`/games/${gameData.id}/review`}>
                    <Button size="lg" className="gap-2">
                      <Star className="h-4 w-4" />
                      Avaliar Jogo
                    </Button>
                  </Link>
                  
                  <Button size="lg" variant="outline" className="gap-2">
                    <ExternalLink className="h-4 w-4" />
                    Comprar
                  </Button>
                </div>
              </div>
            </div>
            
            {/* Price History Chart */}
            <PriceHistoryChart data={priceHistory} />
            
            {/* Reviews Section */}
            <div>
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold">Avaliações dos Usuários</h2>
                <Link href={`/games/${gameData.id}/reviews`}>
                  <Button variant="outline">Ver todas</Button>
                </Link>
              </div>
              
              <div className="space-y-4">
                {reviews.map((review) => (
                  <ReviewCard key={review.id} {...review} />
                ))}
              </div>
            </div>
          </div>
          
          {/* Right Column - Actions */}
          <div className="space-y-6">
            {/* Price Monitoring Card */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Bell className="h-5 w-5" />
                  Monitorar Preço
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <TrendingDown className="h-4 w-4 text-accent" />
                    <span className="text-sm font-medium">Menor preço histórico</span>
                  </div>
                  <div className="text-2xl font-bold text-accent">${gameData.lowestPrice}</div>
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="target-price">Preço desejado</Label>
                  <Input
                    id="target-price"
                    type="number"
                    placeholder="39.99"
                    step="0.01"
                  />
                </div>
                
                <Button className="w-full gap-2">
                  <Bell className="h-4 w-4" />
                  Adicionar à Watchlist
                </Button>
                
                <p className="text-xs text-muted-foreground text-center">
                  Você será notificado quando o preço atingir seu valor alvo
                </p>
              </CardContent>
            </Card>
            
            {/* Game Stats */}
            <Card>
              <CardHeader>
                <CardTitle>Estatísticas</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground">Avaliações</span>
                  <span className="font-semibold">{gameData.totalReviews}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground">Nota média</span>
                  <span className="font-semibold">{gameData.averageRating}/10</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground">Monitorando</span>
                  <span className="font-semibold">342 usuários</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground">Lançamento</span>
                  <span className="font-semibold text-sm">{gameData.releaseDate}</span>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  )
}
